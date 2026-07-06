# Random

Random is an AI tool that helps architects and engineers in East Africa design, check compliance, and prepare documentation quickly and efficiently.
It provides references to regional building codes, automated compliance checks, and sample workflows for engineers and architects.

What It Does
- Generate concept drawings adapted to tropical climates and local materials  
- Check designs against Uganda Building Code 2024 and South Sudan guidelines  
- Create simple reports, proposals, and compliance checklists  
- Support collaboration through GitHub workflows
  

Repo Structure

├── docs/              (Regional building codes and standards references)
├── src/               (Core bot logic)
├── workflows/         (Predefined workflows (concepts, compliance, docs))
├── examples/          (Sample usage scripts)
├── tests/             (Unit tests)
├── README.md          (Project overview)
└── LICENSE           (License file)


Final Repo Structure (Extended)
ai-architecture-bot/
│
├── src/
│   ├── core/
│   │   ├── engine.py              # Workflow engine (runs stages)
│   │   ├── context.py             # Shared memory/state handler
│   │   └── dispatcher.py          # Routes tasks between stages
│   │
│   ├── stages/
│   │   ├── concept_stage.py       # Idea generation (design thinking)
│   │   ├── compliance_stage.py    # Rules, safety, building codes
│   │   ├── analysis_stage.py      # Climate, cost, feasibility logic
│   │   └── output_stage.py        # Final architectural plan output
│   │
│   ├── models/
│   │   ├── prompt_models.py       # Prompt templates for AI generation
│   │   └── design_schema.py       # Structure of architectural output
│   │
│   ├── utils/
│   │   ├── logger.py              # Debug + workflow tracking
│   │   ├── validators.py          # Input/output validation
│   │   └── helpers.py             # Small reusable tools
│   │
│   └── main.py                    # Entry point (run system here)
│
├── workflows/
│   ├── basic_design.json          # Simple architecture pipeline
│   ├── eco_building.json          # Eco-friendly workflow
│   └── urban_plan.json            # Large-scale city design flow
│
├── docs/
│   ├── building_codes/
│   │   ├── global_standards.md
│   │   ├── tropical_climate.md
│   │   └── fire_safety_rules.md
│   │
│   ├── system_design.md
│   └── architecture_notes.md
│
├── examples/
│   ├── run_basic.py
│   ├── run_eco.py
│   └── sample_inputs.json
│
├── tests/
│   ├── test_engine.py
│   ├── test_stages.py
│   └── test_workflows.py
│
├── config/
│   ├── settings.py               # Global config
│   └── api_keys.env.example
│
├── requirements.txt
├── README.md
└── .gitignore


RANDOM/
│
├── streamlit_app.py
│
├── engine/
│   ├── evolution.py
│   ├── optimizer.py
│   ├── genetics.py
│   ├── planner.py
│   └── scoring.py
│
├── agents/
│   ├── architect.py
│   ├── structural.py
│   ├── boq.py
│   ├── code_checker.py
│   ├── sustainability.py
│   └── project_manager.py
│
├── bim/
│   ├── building.py
│   ├── floor.py
│   ├── room.py
│   ├── wall.py
│   ├── slab.py
│   └── roof.py
│
├── visualization/
│   ├── floorplan.py
│   ├── renderer2d.py
│   ├── renderer3d.py
│   └── dashboard.py
│
├── memory/
│   ├── memory.json
│   ├── learning.py
│   └── history.py
│
├── data/
│
├── exports/
│
├── reports/
│
└── plugins/


🏠 Project Overview

📐 Floor Plan

🏗 Structural Model

💰 Cost Estimate

🌍 Sustainability

📋 Code Compliance

📊 AI Evolution

🧠 Memory

⚙ Settings

v33-simulation-os/
│
├── streamlit_app.py                # UI entrypoint only (thin shell)
├── requirements.txt
├── README.md
│
├── core/                           # 🧠 central simulation kernel
│   ├── __init__.py
│   ├── config.py                   # global constants + runtime config
│   ├── engine.py                   # main simulation loop
│   ├── scheduler.py                # tick system / time control
│   └── registry.py                 # module/plugin registry
│
├── world/                          # 🌐 voxel + physics system
│   ├── __init__.py
│   ├── voxel.py                    # voxel grid representation
│   ├── terrain.py                  # terrain generation
│   ├── biomes.py                  # biome rules
│   ├── fluids.py                  # water + flow simulation
│   ├── erosion.py                 # terrain decay system
│   └── renderer.py                # projection + visualization
│
├── agents/                         # 🤖 civilization layer
│   ├── __init__.py
│   ├── agent.py                   # base agent class
│   ├── behavior.py                # decision logic
│   ├── movement.py                # navigation system
│   └── society.py                 # grouping + social structures
│
├── architecture/                   # 🏗 generative design engine
│   ├── __init__.py
│   ├── genome.py                  # building DNA system
│   ├── generator.py               # procedural design creation
│   ├── mutation.py                # evolutionary operators
│   ├── fitness.py                # scoring functions
│   └── floorplans.py             # spatial layout generation
│
├── evolution/                     # 🧬 meta-learning system
│   ├── __init__.py
│   ├── evolutionary_loop.py       # selection cycle
│   ├── population.py              # population management
│   ├── selection.py               # survival logic
│   └── adaptive_rules.py          # self-modifying parameters
│
├── meta/                          # 🧠 system that changes system
│   ├── __init__.py
│   ├── rule_engine.py             # dynamic rule mutation
│   ├── observation.py             # system monitoring
│   ├── diagnostics.py             # anomaly detection
│   └── self_tuner.py              # auto-optimization logic
│
├── memory/                        # 💾 persistence layer
│   ├── __init__.py
│   ├── store.py                  # JSON / disk storage
│   ├── logger.py                 # event logging system
│   └── snapshot.py               # world state snapshots
│
├── ui/                           # 🎛 streamlit interface layer
│   ├── __init__.py
│   ├── dashboard.py
│   ├── world_view.py
│   ├── architecture_view.py
│   ├── agent_view.py
│   └── memory_view.py
│
├── plugins/                     # 🔌 extensibility layer
│   ├── __init__.py
│   ├── base_plugin.py
│   └── example_plugin.py
│
└── tests/                       # 🧪 system validation
    ├── test_world.py
    ├── test_agents.py
    ├── test_architecture.py
    └── test_evolution.py

plugins/
    council/
        structural_agent.py
        cost_agent.py
        spatial_agent.py
        aesthetic_agent.py
        council_orchestrator.py