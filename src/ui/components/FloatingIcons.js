// import React, { useState, useEffect, useRef } from 'react';
// import { FaPlane, FaGlobeAmericas, FaMapMarkerAlt, FaPlaneDeparture, FaPlaneArrival } from 'react-icons/fa';
// import './FloatingIcons.css';

// const FloatingIcons = () => {
//   const [icons, setIcons] = useState([]);
//   const containerRef = useRef(null);
//   const mousePosition = useRef({ x: 0, y: 0 });
//   const animationFrameId = useRef();

//   // Icons with their properties - slower movement, less spinning
//   const iconTypes = [
//     { icon: FaPlane, size: 42, speed: 0.005, distance: 40, rotation: 5 },
//     { icon: FaGlobeAmericas, size: 50, speed: 0.003, distance: 50, rotation: 2 },
//     { icon: FaMapMarkerAlt, size: 38, speed: 0.007, distance: 35, rotation: 3 },
//     { icon: FaPlaneDeparture, size: 46, speed: 0.004, distance: 45, rotation: 4 },
//     { icon: FaPlaneArrival, size: 46, speed: 0.006, distance: 40, rotation: 4 },
//   ];

//   // Initialize icons with random positions
//   useEffect(() => {
//     if (containerRef.current) {
//       const containerRect = containerRef.current.getBoundingClientRect();
//       const newIcons = iconTypes.map((iconType, index) => ({
//         ...iconType,
//         id: index,
//         x: Math.random() * (containerRect.width - 100) + 50,
//         y: Math.random() * (containerRect.height - 100) + 50,
//         targetX: 0,
//         targetY: 0,
//         vx: 0,
//         vy: 0,
//       }));
//       setIcons(newIcons);
//     }
//   }, []);

//   // Handle mouse movement
//   useEffect(() => {
//     const handleMouseMove = (e) => {
//       mousePosition.current = { x: e.clientX, y: e.clientY };
//     };

//     window.addEventListener('mousemove', handleMouseMove);
//     return () => window.removeEventListener('mousemove', handleMouseMove);
//   }, []);

//   // Animation loop
//   useEffect(() => {
//     if (icons.length === 0) return;

//     const animate = () => {
//       setIcons(prevIcons => 
//         prevIcons.map(icon => {
//           // Calculate distance to mouse
//           const dx = mousePosition.current.x - icon.x;
//           const dy = mousePosition.current.y - icon.y;
//           const distance = Math.sqrt(dx * dx + dy * dy);

//           // If mouse is very close, move away (reduced sensitivity and force)
//           if (distance < 250) {
//             const angle = Math.atan2(dy, dx);
//             const force = Math.max(0, (250 - distance) * 0.02); // Further reduced force
//             icon.targetX = icon.x - Math.cos(angle) * force;
//             icon.targetY = icon.y - Math.sin(angle) * force;
//           } else {
//             // Slower, more subtle floating movement
//             icon.targetX = icon.x + Math.sin(Date.now() * icon.speed) * 5;
//             icon.targetY = icon.y + Math.cos(Date.now() * icon.speed * 0.8) * 5;
//           }

//           // Even smoother, slower movement
//           icon.vx += (icon.targetX - icon.x) * 0.04; // Further reduced movement speed
//           icon.vy += (icon.targetY - icon.y) * 0.04;
          
//           // Apply more friction for smoother, less bouncy movement
//           icon.vx *= 0.95;
//           icon.vy *= 0.95;
          
//           // Limit maximum velocity for smoother movement
//           const maxVelocity = 0.5;
//           icon.vx = Math.max(-maxVelocity, Math.min(icon.vx, maxVelocity));
//           icon.vy = Math.max(-maxVelocity, Math.min(icon.vy, maxVelocity));
          
//           // Update position
//           icon.x += icon.vx;
//           icon.y += icon.vy;

//           return { ...icon };
//         })
//       );
      
//       animationFrameId.current = requestAnimationFrame(animate);
//     };

//     animationFrameId.current = requestAnimationFrame(animate);
//     return () => cancelAnimationFrame(animationFrameId.current);
//   }, [icons.length]);

//   return (
//     <div ref={containerRef} className="floating-icons-container">
//       {icons.map(({ id, icon: Icon, x, y, size, rotation = 0 }) => {
//         // Calculate rotation based on velocity for more natural movement
//         const rotationAngle = Math.atan2(icons[id]?.vy || 0, icons[id]?.vx || 0) * (180 / Math.PI);
        
//         return (
//           <div
//             key={id}
//             className="floating-icon"
//             style={{
//               transform: `translate3d(${x}px, ${y}px, 0) rotate(${rotationAngle}deg)`,
//               width: `${size}px`,
//               height: `${size}px`,
//               color: `rgba(255, 255, 255, ${0.4 + Math.random() * 0.3})`,
//               transition: 'transform 0.5s ease-out',
//             }}
//           >
//             <Icon className="icon" style={{ transform: `rotate(${-rotationAngle}deg)` }} />
//           </div>
//         );
//       })}
//     </div>
//   );
// };

// export default FloatingIcons;
