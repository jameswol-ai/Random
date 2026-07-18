import json

def generate_threejs_html(rooms):
    """Generate HTML with Three.js 3D viewer."""
    if not rooms:
        return ""
    
    # Convert rooms to 3D boxes (extruded)
    boxes = []
    for r in rooms:
        boxes.append({
            "x": r["x"],
            "z": r["y"],  # Three.js uses x,z for ground plane
            "w": r["w"],
            "d": r["h"],
            "h": 3.0,  # floor height
            "color": r["color"]
        })
    
    boxes_json = json.dumps(boxes)
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background: #1a1a2e; }}
            #info {{ position: absolute; top: 10px; left: 50%; transform: translateX(-50%); color: white; font-family: Arial; font-size: 14px; background: rgba(0,0,0,0.5); padding: 8px 16px; border-radius: 20px; }}
        </style>
    </head>
    <body>
        <div id="info">🔄 Drag to rotate • Scroll to zoom</div>
        <script type="importmap">
        {{
            "imports": {{
                "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
                "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
            }}
        }}
        </script>
        <script type="module">
            import * as THREE from 'three';
            import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
            import {{ CSS2DRenderer, CSS2DObject }} from 'three/addons/renderers/CSS2DRenderer.js';
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x1a1a2e);
            
            const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
            camera.position.set(18, 14, 18);
            camera.lookAt(0, 0, 0);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            document.body.appendChild(renderer.domElement);
            
            const labelRenderer = new CSS2DRenderer();
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.domElement.style.position = 'absolute';
            labelRenderer.domElement.style.top = '0px';
            labelRenderer.domElement.style.left = '0px';
            labelRenderer.domElement.style.pointerEvents = 'none';
            document.body.appendChild(labelRenderer.domElement);
            
            // Controls
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.08;
            controls.target.set(0, 1.5, 0);
            
            // Lights
            const ambient = new THREE.AmbientLight(0x404060);
            scene.add(ambient);
            
            const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
            dirLight.position.set(10, 20, 10);
            dirLight.castShadow = true;
            scene.add(dirLight);
            
            const fillLight = new THREE.DirectionalLight(0x88aaff, 0.5);
            fillLight.position.set(-10, 5, -10);
            scene.add(fillLight);
            
            // Grid
            const grid = new THREE.GridHelper(30, 20, 0x88aaff, 0x444466);
            grid.position.y = -0.01;
            scene.add(grid);
            
            // Boxes
            const boxes = {boxes_json};
            const geometries = [];
            
            boxes.forEach(b => {{
                const geo = new THREE.BoxGeometry(b.w, b.h, b.d);
                const mat = new THREE.MeshStandardMaterial({{
                    color: b.color,
                    roughness: 0.3,
                    metalness: 0.1,
                    transparent: true,
                    opacity: 0.85
                }});
                const mesh = new THREE.Mesh(geo, mat);
                mesh.position.set(b.x + b.w/2, b.h/2, b.z + b.d/2);
                mesh.castShadow = true;
                mesh.receiveShadow = true;
                scene.add(mesh);
                
                // Edges (wireframe)
                const edges = new THREE.EdgesGeometry(geo);
                const lineMat = new THREE.LineBasicMaterial({{ color: 0xffffff, transparent: true, opacity: 0.3 }});
                const wireframe = new THREE.LineSegments(edges, lineMat);
                wireframe.position.copy(mesh.position);
                scene.add(wireframe);
                
                // Label (CSS2D)
                const div = document.createElement('div');
                div.textContent = b.name || 'Room';
                div.style.color = 'white';
                div.style.fontFamily = 'Arial';
                div.style.fontSize = '12px';
                div.style.fontWeight = 'bold';
                div.style.textShadow = '0 0 10px rgba(0,0,0,0.8)';
                div.style.background = 'rgba(0,0,0,0.5)';
                div.style.padding = '2px 8px';
                div.style.borderRadius = '12px';
                div.style.pointerEvents = 'none';
                
                const label = new CSS2DObject(div);
                label.position.set(b.x + b.w/2, b.h + 0.3, b.z + b.d/2);
                scene.add(label);
            }});
            
            // Floor (semi-transparent)
            const floorGeo = new THREE.PlaneGeometry(25, 25);
            const floorMat = new THREE.MeshStandardMaterial({{
                color: 0x222244,
                transparent: true,
                opacity: 0.3,
                roughness: 0.5,
                metalness: 0.1,
                side: THREE.DoubleSide
            }});
            const floor = new THREE.Mesh(floorGeo, floorMat);
            floor.rotation.x = -Math.PI / 2;
            floor.position.set(0, 0, 0);
            scene.add(floor);
            
            // Animation
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
                labelRenderer.render(scene, camera);
            }}
            animate();
            
            // Resize handler
            window.addEventListener('resize', () => {{
                const w = window.innerWidth;
                const h = window.innerHeight;
                camera.aspect = w / h;
                camera.updateProjectionMatrix();
                renderer.setSize(w, h);
                labelRenderer.setSize(w, h);
            }});
        </script>
    </body>
    </html>
    '''
    return html