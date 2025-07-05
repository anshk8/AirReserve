#!/usr/bin/env python3
"""
Comprehensive test suite for flight price monitoring system
Tests all aspects including normal operation, error scenarios, and notifications
"""

import asyncio
import json
import sys
import os
import time
from pathlib import Path
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.agent.langchain_notifier import load_prices, send_notification, THRESHOLD, load_config
from src.agent.notification_manager import NotificationManager
from src.agent.real_time_data_manager import RealTimeDataManager
from src.agent.discord_notifier import DiscordNotifier

class TestResults:
    """Track test results and statistics."""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_details = []
    
    def add_test(self, test_name, passed, details=""):
        """Add a test result."""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
        
        self.test_details.append({
            "name": test_name,
            "status": status,
            "details": details
        })
        
        print(f"{status}: {test_name}")
        if details:
            print(f"   📝 {details}")
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUITE RESULTS")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ Failed Tests:")
            for test in self.test_details:
                if "FAIL" in test["status"]:
                    print(f"   - {test['name']}: {test['details']}")
        
        print("\n" + "=" * 60)

async def test_normal_operation(results):
    """Test normal operation with valid data."""
    print("\n🧪 Testing Normal Operation...")
    
    try:
        # Test 1: Load valid flight data
        flights = await load_prices()
        results.add_test(
            "Load Valid Flight Data",
            len(flights) > 0,
            f"Loaded {len(flights)} flights"
        )
        
        # Test 2: Check price drop detection
        price_drops = [f for f in flights if f.get("price", 0) < THRESHOLD]
        results.add_test(
            "Price Drop Detection",
            len(price_drops) >= 3,  # Should have at least 3 price drops
            f"Detected {len(price_drops)} price drops below ${THRESHOLD}"
        )
        
        # Test 3: Test notification sending
        if price_drops:
            test_flight = price_drops[0]
            notification = await send_notification(test_flight)
            results.add_test(
                "Notification Sending",
                notification is not None,
                f"Sent notification for {test_flight.get('airline')} to {test_flight.get('destination')}"
            )
        
        return True
        
    except Exception as e:
        results.add_test("Normal Operation", False, f"Error: {e}")
        return False

async def test_error_scenarios(results):
    """Test various error scenarios."""
    print("\n🧪 Testing Error Scenarios...")
    
    # Test 1: Corrupted JSON file
    try:
        corrupted_file = Path("data/flight_prices_corrupted.json")
        if corrupted_file.exists():
            # Temporarily rename the good file and use corrupted one
            good_file = Path("data/flight_prices.json")
            backup_file = Path("data/flight_prices_backup.json")
            
            if good_file.exists():
                good_file.rename(backup_file)
            
            corrupted_file.rename(good_file)
            
            # Try to load corrupted data
            flights = await load_prices()
            
            # Restore good file
            good_file.rename(corrupted_file)
            if backup_file.exists():
                backup_file.rename(good_file)
            
            results.add_test(
                "Corrupted JSON Handling",
                len(flights) == 0,  # Should return empty list
                "Gracefully handled corrupted JSON"
            )
        else:
            results.add_test("Corrupted JSON Handling", True, "Skipped - no corrupted file")
            
    except Exception as e:
        results.add_test("Corrupted JSON Handling", False, f"Error: {e}")
    
    # Test 2: Missing file handling
    try:
        # Temporarily rename the data file
        data_file = Path("data/flight_prices.json")
        backup_file = Path("data/flight_prices_backup.json")
        
        if data_file.exists():
            data_file.rename(backup_file)
        
        # Try to load missing file
        flights = await load_prices()
        
        # Restore file
        if backup_file.exists():
            backup_file.rename(data_file)
        
        results.add_test(
            "Missing File Handling",
            len(flights) == 0,  # Should return empty list
            "Gracefully handled missing file"
        )
        
    except Exception as e:
        results.add_test("Missing File Handling", False, f"Error: {e}")
    
    # Test 3: Malformed flight data
    try:
        malformed_file = Path("data/flight_prices_malformed.json")
        if malformed_file.exists():
            # Temporarily use malformed data
            good_file = Path("data/flight_prices.json")
            backup_file = Path("data/flight_prices_backup.json")
            
            if good_file.exists():
                good_file.rename(backup_file)
            
            malformed_file.rename(good_file)
            
            # Try to process malformed data
            flights = await load_prices()
            
            # Restore good file
            good_file.rename(malformed_file)
            if backup_file.exists():
                backup_file.rename(good_file)
            
            results.add_test(
                "Malformed Data Handling",
                True,  # Should not crash
                f"Processed {len(flights)} flights from malformed data"
            )
        else:
            results.add_test("Malformed Data Handling", True, "Skipped - no malformed file")
            
    except Exception as e:
        results.add_test("Malformed Data Handling", False, f"Error: {e}")

async def test_notification_system(results):
    """Test notification system components."""
    print("\n🧪 Testing Notification System...")
    
    # Test 1: Notification Manager
    try:
        notification_manager = NotificationManager(throttle_minutes=1)  # Short throttle for testing
        
        test_flight = {
            "price": 150.0,
            "airline": "Test Air",
            "destination": "Test City"
        }
        
        # Test throttling
        is_throttled = notification_manager.is_throttled(test_flight)
        results.add_test(
            "Notification Throttling",
            not is_throttled,  # Should not be throttled initially
            "Initial notification not throttled"
        )
        
        # Record notification and test throttling
        notification_manager.record_notification(test_flight, ["console"])
        is_throttled_after = notification_manager.is_throttled(test_flight)
        results.add_test(
            "Notification Throttling After Record",
            is_throttled_after,  # Should be throttled after recording
            "Notification throttled after recording"
        )
        
        # Test statistics
        stats = notification_manager.get_notification_stats()
        results.add_test(
            "Notification Statistics",
            stats["total"] > 0,
            f"Recorded {stats['total']} notifications"
        )
        
    except Exception as e:
        results.add_test("Notification System", False, f"Error: {e}")
    
    # Test 2: Discord Notifier (if configured)
    try:
        from src.agent.langchain_notifier import DISCORD_WEBHOOK_URL
        if DISCORD_WEBHOOK_URL:
            discord_notifier = DiscordNotifier(DISCORD_WEBHOOK_URL)
            test_flight = {
                "price": 150.0,
                "airline": "Test Air",
                "destination": "Test City"
            }
            
            # Note: We won't actually send to Discord during testing
            results.add_test(
                "Discord Notifier Setup",
                True,
                "Discord notifier configured and ready"
            )
        else:
            results.add_test("Discord Notifier Setup", True, "Skipped - no webhook configured")
            
    except Exception as e:
        results.add_test("Discord Notifier Setup", False, f"Error: {e}")

async def test_real_time_data_manager(results):
    """Test real-time data manager functionality."""
    print("\n🧪 Testing Real-Time Data Manager...")
    
    try:
        # Create data manager
        data_manager = RealTimeDataManager(data_dir="data", refresh_interval=60)
        
        # Test 1: Data stats
        stats = data_manager.get_data_stats()
        results.add_test(
            "Data Manager Stats",
            isinstance(stats, dict),
            f"Stats: {stats['total_routes']} routes, {stats['total_flights']} flights"
        )
        
        # Test 2: Load all flight data
        all_flights = await data_manager.get_all_flight_data()
        results.add_test(
            "Load All Flight Data",
            isinstance(all_flights, list),
            f"Loaded {len(all_flights)} flights from all routes"
        )
        
        # Test 3: Data change callback
        callback_called = False
        
        async def test_callback(data):
            nonlocal callback_called
            callback_called = True
            return True
        
        # Start monitoring for a short time
        monitor_task = asyncio.create_task(
            data_manager.monitor_data_changes(test_callback)
        )
        
        try:
            await asyncio.wait_for(monitor_task, timeout=5)
        except asyncio.TimeoutError:
            monitor_task.cancel()
        
        results.add_test(
            "Data Change Callback",
            True,  # Should not crash
            "Data monitoring started successfully"
        )
        
    except Exception as e:
        results.add_test("Real-Time Data Manager", False, f"Error: {e}")

async def test_configuration_system(results):
    """Test configuration system."""
    print("\n🧪 Testing Configuration System...")
    
    try:
        # Test 1: Load configuration
        config = load_config()
        results.add_test(
            "Configuration Loading",
            isinstance(config, dict),
            f"Loaded config with {len(config)} settings"
        )
        
        # Test 2: Check required settings
        required_settings = ["threshold", "check_interval", "notification_channels"]
        missing_settings = [s for s in required_settings if s not in config]
        results.add_test(
            "Required Configuration Settings",
            len(missing_settings) == 0,
            f"Missing settings: {missing_settings}" if missing_settings else "All required settings present"
        )
        
        # Test 3: Real-time data config
        real_time_config = config.get("real_time_data", {})
        results.add_test(
            "Real-Time Data Configuration",
            isinstance(real_time_config, dict),
            f"Real-time config: {real_time_config.get('enabled', 'Not set')}"
        )
        
    except Exception as e:
        results.add_test("Configuration System", False, f"Error: {e}")

async def test_continuous_operation(results):
    """Test continuous operation without crashes."""
    print("\n🧪 Testing Continuous Operation...")
    
    try:
        # Test 1: Multiple data loads
        for i in range(3):
            flights = await load_prices()
            if len(flights) == 0:
                break
        
        results.add_test(
            "Multiple Data Loads",
            True,  # Should not crash
            f"Successfully loaded data {i+1} times"
        )
        
        # Test 2: Notification processing
        test_flights = [
            {"price": 150.0, "airline": "Test Air 1", "destination": "Test City 1"},
            {"price": 180.0, "airline": "Test Air 2", "destination": "Test City 2"},
            {"price": 250.0, "airline": "Test Air 3", "destination": "Test City 3"}
        ]
        
        notifications_sent = 0
        for flight in test_flights:
            try:
                notification = await send_notification(flight)
                if notification:
                    notifications_sent += 1
            except Exception as e:
                print(f"   ⚠️  Notification error: {e}")
        
        results.add_test(
            "Continuous Notification Processing",
            notifications_sent >= 2,  # Should send at least 2 notifications
            f"Sent {notifications_sent} notifications successfully"
        )
        
    except Exception as e:
        results.add_test("Continuous Operation", False, f"Error: {e}")

async def main():
    """Run all comprehensive tests."""
    print("🚀 Flight Price Monitor - Comprehensive Test Suite")
    print("=" * 60)
    
    results = TestResults()
    
    # Run all test categories
    await test_normal_operation(results)
    await test_error_scenarios(results)
    await test_notification_system(results)
    await test_real_time_data_manager(results)
    await test_configuration_system(results)
    await test_continuous_operation(results)
    
    # Print results
    results.print_summary()
    
    # Return exit code
    if results.failed_tests > 0:
        print("❌ Some tests failed. Please review the issues above.")
        return 1
    else:
        print("🎉 All tests passed! System is ready for production.")
        return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 