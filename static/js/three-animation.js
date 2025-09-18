// Three.js Animation for VSK Gujarat Website

let scene, camera, renderer, particles;

function initThree() {
    // Check if canvas element exists
    const canvas = document.getElementById('three-canvas');
    if (!canvas) return;

    // Setup
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true });

    renderer.setSize(window.innerWidth, window.innerHeight);

    // Create particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 5000;

    const posArray = new Float32Array(particlesCount * 3);
    const colorArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        // Position
        posArray[i] = (Math.random() - 0.5) * 100;

        // Color
        colorArray[i] = Math.random();
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorArray, 3));

    // Material
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.05,
        vertexColors: true,
        transparent: true,
        opacity: 0.8
    });

    // Points system
    particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);

    camera.position.z = 5;

    // Mouse movement
    let mouseX = 0;
    let mouseY = 0;

    document.addEventListener('mousemove', (event) => {
        mouseX = event.clientX / window.innerWidth * 2 - 1;
        mouseY = -(event.clientY / window.innerHeight * 2 - 1);
    });

    // Animation
    function animate() {
        requestAnimationFrame(animate);

        particles.rotation.x += 0.0005;
        particles.rotation.y += 0.001;

        camera.position.x += (mouseX * 5 - camera.position.x) * 0.01;
        camera.position.y += (mouseY * 5 - camera.position.y) * 0.01;

        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    animate();

    // Resize handler
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// Initialize Three.js when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a page with Three.js canvas
    if (document.getElementById('three-canvas')) {
        initThree();
    }
});