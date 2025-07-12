1. Use Node.js with npm for our build system.
2. Use Jest for unit and integration testing.
3. Don't modify files in /config or /data directories.
4. Use only Tavily's web crawl API for flight data.
5. Parse user inputs for flight details, validating IATA codes, ISO 8601 dates, and budgets.
6. Return JSON with "clarification_needed" for unclear inputs.
7. Limit API requests to 5 per second, cache in SQLite with 24-hour TTL.
8. Retry failed API calls once after 2 seconds, then send error message.
9. Queue up to 10 background booking tasks, log failures in “windsurf_errors.log.”
10. Deliver JSON or text responses in under 2 seconds, bundle code in .zip for judges.



Deliver JSON or text responses in under 2 seconds, bundle code in .zip for judges.