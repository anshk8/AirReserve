const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Setting up AirReserve development environment...');

// Create necessary directories if they don't exist
const directories = [
  'public',
  'src/ui/components',
  'src/ui/styles',
  'dist'
];

directories.forEach(dir => {
  const dirPath = path.join(__dirname, '..', dir);
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`Created directory: ${dirPath}`);
  }
});

console.log('Installing Node.js dependencies...');

// Install Node.js dependencies
exec('npm install', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error installing dependencies: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`stderr: ${stderr}`);
    return;
  }
  console.log(stdout);
  
  console.log('\n✅ Setup completed successfully!');
  console.log('\nTo start the development server, run:');
  console.log('  npm run dev');
  console.log('\nThen open http://localhost:3000 in your browser.');
});
