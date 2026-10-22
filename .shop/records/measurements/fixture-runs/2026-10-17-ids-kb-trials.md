---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-17-ids-kb-trials
kind: measurement
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration, capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency]
date: 2026-10-17
---

# kb clone trials: adding ids (kbtrial, kbtrial2) and a consistency report (kbtrial3)

The inputs and small outputs of three headless trials on clones of shopsystem-kb (2026-10-17), run from the fixture harness's directory with plugin B: `kbtrial` and `kbtrial2` asked `migrating-to-capabilities` to add `[r<n>]` ids (kbtrial with the 0.19.0 wording "context id", kbtrial2 with the type-first wording "context path"; the test log `2026-10-16-requirement-ids-test-log.md`, "kb clone trial 2", reports kbtrial2: $4.33 over two sessions, 371 lines numbered, 361 scenarios tagged, commit `a52b712`), and `kbtrial3` ran `checking-spec-consistency` in report mode on the id-migrated clone (reported in `2026-10-17-ubiquitous-language-test-log.md`, "kb report-mode run": $3.28, 77 findings). `dev.log` is the clone's `make dev` output; `counts.txt` the baseline's scenario count per slice tag (`kbtrial2-baseline/count.txt` is byte-identical). Every stderr*.log was empty. Left in scratch: the clones (`repo/`), the transcripts, the baseline feature files (a copy of shopsystem-kb `features/` at commit `9f62b5a`) and the baseline pytest outputs (1603 passed, reproducible from that commit).

Archived from git-ignored scratch; each file's text as it was.

## `/home/vscode/scratch/shopsystem-bdd/ids/kbtrial/prompt.txt`

~~~~~~
This repository is on capability files, but its Behaviour lines carry no [r<n>] ids. Use shopsystem-bdd:migrating-to-capabilities to add them. The context id is missingmass.io/shopsystem/kb: the owner's domain missingmass.io, the product shopsystem, the context kb; that is my answer for the gate's context id. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. If the gate has any question beyond the context id, stop at the gate and show me every question with its readings; commit nothing past what the skill allows before the gate. Otherwise carry on and stop when it is committed. I am away: ask me nothing and wait for nothing.
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/kbtrial2/prompt.txt`

~~~~~~
This repository is on capability files, but its Behaviour lines carry no [r<n>] ids. Use shopsystem-bdd:migrating-to-capabilities to add them. The context path is missingmass.io/shopsystem/kb: the owner's domain missingmass.io, the product shopsystem, the context kb; that is my answer for the gate's context path. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. If the gate has any question beyond the context id, stop at the gate and show me every question with its readings; commit nothing past what the skill allows before the gate. Otherwise carry on and stop when it is committed. I am away: ask me nothing and wait for nothing.
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/kbtrial3/prompt.txt`

~~~~~~
Use shopsystem-bdd:checking-spec-consistency in report mode on this repository's spec. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop when the findings are written. I am away: ask me nothing and wait for nothing.
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/kbtrial/baseline-ids/counts.txt`

~~~~~~
slice-1 3
slice-1.2 1
slice-1.3 1
slice-1.4 1
slice-1.6 4
slice-1.7 2
slice-1.8 4
slice-1.10 1
slice-1.11 1
slice-1.12 1
slice-1.13 2
slice-1.15 1
slice-1.16 1
slice-1.21 1
slice-1.22 1
slice-1.23 1
slice-1.25 1
slice-1.26 2
slice-3 1
slice-6 1
slice-8 1
slice-9 1
slice-10 1
slice-11 1
slice-12 1
slice-13 1
slice-14 1
slice-21 6
slice-23 2
slice-25 1
slice-27 1
slice-29 3
slice-31 2
slice-33 2
slice-35 3
slice-37 1
slice-39 8
slice-41 3
slice-43 1
slice-45 3
slice-46 9
slice-65 4
slice-66 1
slice-67 3
slice-70 1
slice-71 3
slice-72 1
slice-73 1
slice-75 8
slice-77 1
slice-78 1
slice-85 2
slice-86 2
slice-87 1
slice-88 6
slice-89 1
slice-89.2 1
slice-91 4
slice-92 1
slice-93 6
slice-94 3
slice-96 20
slice-97 1
slice-99 5
slice-102 7
slice-102.3 5
slice-102.4 8
slice-104 1
slice-105 2
slice-106 1
slice-110 3
slice-111 4
slice-112 15
slice-115 6
slice-116 5
slice-117 1
slice-118.2 3
slice-118.3 1
slice-118.4 3
slice-121 4
slice-122 17
slice-124 6
slice-125 12
slice-126 5
slice-128 7
slice-128.1 3
slice-129 4
slice-130 1
slice-131 5
slice-132 3
slice-133 4
slice-133.1 1
slice-134 8
slice-135 3
slice-136 2
slice-137 1
slice-138 1
slice-139 1
slice-140 5
slice-141 2
slice-142 4
slice-143 6
slice-144 2
slice-146 3
slice-148 2
slice-149 3
slice-150 4
slice-151 6
slice-152 1
slice-153 13
slice-156 6
slice-157 1
slice-158 8
slice-159 3
slice-160 7
slice-161 4
slice-162 3
slice-163 8
slice-163.1 3
slice-163.2 1
slice-164 4
slice-165 6
slice-165.1 2
slice-165.3 3
slice-165.6 1
slice-166 3
slice-166.1 2
slice-166.2 1
slice-166.3 2
slice-167 4
slice-168 4
slice-169 5
slice-170 5
slice-170.1 1
slice-171 1
slice-172 2
slice-173 2
slice-174 1
slice-175 2
slice-176 7
slice-177 5
slice-178 18
slice-179 11
slice-180 4
slice-180.2 1
slice-181 3
slice-181.1 1
slice-182 5
slice-182.1 2
slice-183 10
slice-184 9
slice-185 1
total 536
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/kbtrial/dev.log`

~~~~~~
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
Obtaining file:///home/vscode/scratch/shopsystem-bdd/ids/kbtrial/repo
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
Collecting protobuf<8,>=7.35.1 (from shopsystem-kb==0.9.0)
  Using cached protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl.metadata (595 bytes)
Collecting grpcio>=1.84.0 (from shopsystem-kb==0.9.0)
  Using cached grpcio-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (3.8 kB)
Collecting jsonschema>=4.18 (from shopsystem-kb==0.9.0)
  Using cached jsonschema-4.26.0-py3-none-any.whl.metadata (7.6 kB)
Collecting jsonschema-specifications>=2025.9.1 (from shopsystem-kb==0.9.0)
  Using cached jsonschema_specifications-2025.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting referencing>=0.37.0 (from shopsystem-kb==0.9.0)
  Using cached referencing-0.37.0-py3-none-any.whl.metadata (2.8 kB)
Collecting ruamel.yaml<0.20,>=0.19.1 (from shopsystem-kb==0.9.0)
  Using cached ruamel_yaml-0.19.1-py3-none-any.whl.metadata (16 kB)
Collecting pytest<10,>=9 (from shopsystem-kb==0.9.0)
  Using cached pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting pytest-bdd<9,>=8.1.0 (from shopsystem-kb==0.9.0)
  Using cached pytest_bdd-8.1.0-py3-none-any.whl.metadata (53 kB)
Collecting pytest-xdist>=3.6 (from shopsystem-kb==0.9.0)
  Using cached pytest_xdist-3.8.0-py3-none-any.whl.metadata (3.0 kB)
Collecting coverage>=7.6 (from shopsystem-kb==0.9.0)
  Using cached coverage-7.16.2-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (8.2 kB)
Collecting pytest-cov>=6 (from shopsystem-kb==0.9.0)
  Using cached pytest_cov-7.1.0-py3-none-any.whl.metadata (32 kB)
Collecting grpcio-tools>=1.84.0 (from shopsystem-kb==0.9.0)
  Using cached grpcio_tools-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.3 kB)
Collecting typing-extensions~=4.12 (from grpcio>=1.84.0->shopsystem-kb==0.9.0)
  Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Requirement already satisfied: setuptools>=77.0.1 in ./.venv/lib/python3.11/site-packages (from grpcio-tools>=1.84.0->shopsystem-kb==0.9.0) (79.0.1)
Collecting attrs>=22.2.0 (from jsonschema>=4.18->shopsystem-kb==0.9.0)
  Using cached attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting rpds-py>=0.25.0 (from jsonschema>=4.18->shopsystem-kb==0.9.0)
  Using cached rpds_py-2026.9.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.1 kB)
Collecting iniconfig>=1.0.1 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Using cached iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting packaging>=22 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Downloading pluggy-1.7.0-py3-none-any.whl.metadata (5.0 kB)
Collecting pygments>=2.7.2 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Using cached pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
Collecting Mako (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached mako-1.4.3-py3-none-any.whl.metadata (2.9 kB)
Collecting gherkin-official<30.0.0,>=29.0.0 (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached gherkin_official-29.0.0-py3-none-any.whl.metadata (563 bytes)
Collecting parse (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached parse-1.22.3-py2.py3-none-any.whl.metadata (21 kB)
Collecting parse-type (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached parse_type-0.6.6-py2.py3-none-any.whl.metadata (12 kB)
Collecting execnet>=2.1 (from pytest-xdist>=3.6->shopsystem-kb==0.9.0)
  Using cached execnet-2.1.2-py3-none-any.whl.metadata (2.9 kB)
Collecting MarkupSafe>=2.0 (from Mako->pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached markupsafe-3.0.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Collecting six>=1.15 (from parse-type->pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Using cached coverage-7.16.2-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (256 kB)
Using cached grpcio-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (7.2 MB)
Using cached grpcio_tools-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (2.8 MB)
Using cached jsonschema-4.26.0-py3-none-any.whl (90 kB)
Using cached jsonschema_specifications-2025.9.1-py3-none-any.whl (18 kB)
Using cached protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl (343 kB)
Using cached pytest-9.1.1-py3-none-any.whl (386 kB)
Using cached pytest_bdd-8.1.0-py3-none-any.whl (49 kB)
Using cached pytest_cov-7.1.0-py3-none-any.whl (22 kB)
Using cached pytest_xdist-3.8.0-py3-none-any.whl (46 kB)
Using cached referencing-0.37.0-py3-none-any.whl (26 kB)
Using cached ruamel_yaml-0.19.1-py3-none-any.whl (118 kB)
Using cached attrs-26.1.0-py3-none-any.whl (67 kB)
Using cached execnet-2.1.2-py3-none-any.whl (40 kB)
Using cached gherkin_official-29.0.0-py3-none-any.whl (37 kB)
Using cached iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Using cached packaging-26.3-py3-none-any.whl (129 kB)
Downloading pluggy-1.7.0-py3-none-any.whl (27 kB)
Using cached pygments-2.21.0-py3-none-any.whl (1.3 MB)
Using cached rpds_py-2026.9.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (375 kB)
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Using cached mako-1.4.3-py3-none-any.whl (80 kB)
Using cached parse-1.22.3-py2.py3-none-any.whl (21 kB)
Using cached parse_type-0.6.6-py2.py3-none-any.whl (27 kB)
Using cached markupsafe-3.0.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Checking if build backend supports build_editable: started
Checking if build backend supports build_editable: finished with status 'done'
Building wheels for collected packages: shopsystem-kb
  Building editable for shopsystem-kb (pyproject.toml): started
  Building editable for shopsystem-kb (pyproject.toml): finished with status 'done'
  Created wheel for shopsystem-kb: filename=shopsystem_kb-0.9.0-0.editable-py3-none-any.whl size=5965 sha256=dccd5f8c579cd4d3a91573f610aaf09ccfdc0db4047e2528411fe5cf6d03e788
  Stored in directory: /tmp/pip-ephem-wheel-cache-0bf4e9j1/wheels/36/aa/55/461d41307facf64fa23483cecc3d30e727a57c04bc37089109
Successfully built shopsystem-kb
Installing collected packages: parse, gherkin-official, typing-extensions, six, ruamel.yaml, rpds-py, pygments, protobuf, pluggy, packaging, MarkupSafe, iniconfig, execnet, coverage, attrs, referencing, pytest, parse-type, Mako, grpcio, pytest-xdist, pytest-cov, pytest-bdd, jsonschema-specifications, grpcio-tools, jsonschema, shopsystem-kb
Successfully installed Mako-1.4.3 MarkupSafe-3.0.4 attrs-26.1.0 coverage-7.16.2 execnet-2.1.2 gherkin-official-29.0.0 grpcio-1.84.0 grpcio-tools-1.84.0 iniconfig-2.3.1 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 packaging-26.3 parse-1.22.3 parse-type-0.6.6 pluggy-1.7.0 protobuf-7.36.2 pygments-2.21.0 pytest-9.1.1 pytest-bdd-8.1.0 pytest-cov-7.1.0 pytest-xdist-3.8.0 referencing-0.37.0 rpds-py-2026.9.1 ruamel.yaml-0.19.1 shopsystem-kb-0.9.0 six-1.17.0 typing-extensions-4.16.0

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: python3 -m pip install --upgrade pip
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/kbtrial2/dev.log`

~~~~~~
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
Obtaining file:///home/vscode/scratch/shopsystem-bdd/ids/kbtrial2/repo
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
Collecting protobuf<8,>=7.35.1 (from shopsystem-kb==0.9.0)
  Using cached protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl.metadata (595 bytes)
Collecting grpcio>=1.84.0 (from shopsystem-kb==0.9.0)
  Using cached grpcio-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (3.8 kB)
Collecting jsonschema>=4.18 (from shopsystem-kb==0.9.0)
  Using cached jsonschema-4.26.0-py3-none-any.whl.metadata (7.6 kB)
Collecting jsonschema-specifications>=2025.9.1 (from shopsystem-kb==0.9.0)
  Using cached jsonschema_specifications-2025.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting referencing>=0.37.0 (from shopsystem-kb==0.9.0)
  Using cached referencing-0.37.0-py3-none-any.whl.metadata (2.8 kB)
Collecting ruamel.yaml<0.20,>=0.19.1 (from shopsystem-kb==0.9.0)
  Using cached ruamel_yaml-0.19.1-py3-none-any.whl.metadata (16 kB)
Collecting pytest<10,>=9 (from shopsystem-kb==0.9.0)
  Using cached pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting pytest-bdd<9,>=8.1.0 (from shopsystem-kb==0.9.0)
  Using cached pytest_bdd-8.1.0-py3-none-any.whl.metadata (53 kB)
Collecting pytest-xdist>=3.6 (from shopsystem-kb==0.9.0)
  Using cached pytest_xdist-3.8.0-py3-none-any.whl.metadata (3.0 kB)
Collecting coverage>=7.6 (from shopsystem-kb==0.9.0)
  Using cached coverage-7.16.2-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (8.2 kB)
Collecting pytest-cov>=6 (from shopsystem-kb==0.9.0)
  Using cached pytest_cov-7.1.0-py3-none-any.whl.metadata (32 kB)
Collecting grpcio-tools>=1.84.0 (from shopsystem-kb==0.9.0)
  Using cached grpcio_tools-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.3 kB)
Collecting typing-extensions~=4.12 (from grpcio>=1.84.0->shopsystem-kb==0.9.0)
  Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Requirement already satisfied: setuptools>=77.0.1 in ./.venv/lib/python3.11/site-packages (from grpcio-tools>=1.84.0->shopsystem-kb==0.9.0) (79.0.1)
Collecting attrs>=22.2.0 (from jsonschema>=4.18->shopsystem-kb==0.9.0)
  Using cached attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting rpds-py>=0.25.0 (from jsonschema>=4.18->shopsystem-kb==0.9.0)
  Using cached rpds_py-2026.9.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.1 kB)
Collecting iniconfig>=1.0.1 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Using cached iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting packaging>=22 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Using cached pluggy-1.7.0-py3-none-any.whl.metadata (5.0 kB)
Collecting pygments>=2.7.2 (from pytest<10,>=9->shopsystem-kb==0.9.0)
  Using cached pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
Collecting Mako (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached mako-1.4.3-py3-none-any.whl.metadata (2.9 kB)
Collecting gherkin-official<30.0.0,>=29.0.0 (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached gherkin_official-29.0.0-py3-none-any.whl.metadata (563 bytes)
Collecting parse (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached parse-1.22.3-py2.py3-none-any.whl.metadata (21 kB)
Collecting parse-type (from pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached parse_type-0.6.6-py2.py3-none-any.whl.metadata (12 kB)
Collecting execnet>=2.1 (from pytest-xdist>=3.6->shopsystem-kb==0.9.0)
  Using cached execnet-2.1.2-py3-none-any.whl.metadata (2.9 kB)
Collecting MarkupSafe>=2.0 (from Mako->pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached markupsafe-3.0.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Collecting six>=1.15 (from parse-type->pytest-bdd<9,>=8.1.0->shopsystem-kb==0.9.0)
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Using cached coverage-7.16.2-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (256 kB)
Using cached grpcio-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (7.2 MB)
Using cached grpcio_tools-1.84.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (2.8 MB)
Using cached jsonschema-4.26.0-py3-none-any.whl (90 kB)
Using cached jsonschema_specifications-2025.9.1-py3-none-any.whl (18 kB)
Using cached protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl (343 kB)
Using cached pytest-9.1.1-py3-none-any.whl (386 kB)
Using cached pytest_bdd-8.1.0-py3-none-any.whl (49 kB)
Using cached pytest_cov-7.1.0-py3-none-any.whl (22 kB)
Using cached pytest_xdist-3.8.0-py3-none-any.whl (46 kB)
Using cached referencing-0.37.0-py3-none-any.whl (26 kB)
Using cached ruamel_yaml-0.19.1-py3-none-any.whl (118 kB)
Using cached attrs-26.1.0-py3-none-any.whl (67 kB)
Using cached execnet-2.1.2-py3-none-any.whl (40 kB)
Using cached gherkin_official-29.0.0-py3-none-any.whl (37 kB)
Using cached iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Using cached packaging-26.3-py3-none-any.whl (129 kB)
Using cached pluggy-1.7.0-py3-none-any.whl (27 kB)
Using cached pygments-2.21.0-py3-none-any.whl (1.3 MB)
Using cached rpds_py-2026.9.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (375 kB)
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Using cached mako-1.4.3-py3-none-any.whl (80 kB)
Using cached parse-1.22.3-py2.py3-none-any.whl (21 kB)
Using cached parse_type-0.6.6-py2.py3-none-any.whl (27 kB)
Using cached markupsafe-3.0.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Checking if build backend supports build_editable: started
Checking if build backend supports build_editable: finished with status 'done'
Building wheels for collected packages: shopsystem-kb
  Building editable for shopsystem-kb (pyproject.toml): started
  Building editable for shopsystem-kb (pyproject.toml): finished with status 'done'
  Created wheel for shopsystem-kb: filename=shopsystem_kb-0.9.0-0.editable-py3-none-any.whl size=5969 sha256=ac49c53c4cc4cd011a5992e47622037eef31240b06f6be7aa6e28811a747ab1f
  Stored in directory: /tmp/pip-ephem-wheel-cache-2xfm2jc1/wheels/2f/fd/94/813061e665434a48084aa7e1f0a49582a8cc1e5715e9f741a8
Successfully built shopsystem-kb
Installing collected packages: parse, gherkin-official, typing-extensions, six, ruamel.yaml, rpds-py, pygments, protobuf, pluggy, packaging, MarkupSafe, iniconfig, execnet, coverage, attrs, referencing, pytest, parse-type, Mako, grpcio, pytest-xdist, pytest-cov, pytest-bdd, jsonschema-specifications, grpcio-tools, jsonschema, shopsystem-kb
Successfully installed Mako-1.4.3 MarkupSafe-3.0.4 attrs-26.1.0 coverage-7.16.2 execnet-2.1.2 gherkin-official-29.0.0 grpcio-1.84.0 grpcio-tools-1.84.0 iniconfig-2.3.1 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 packaging-26.3 parse-1.22.3 parse-type-0.6.6 pluggy-1.7.0 protobuf-7.36.2 pygments-2.21.0 pytest-9.1.1 pytest-bdd-8.1.0 pytest-cov-7.1.0 pytest-xdist-3.8.0 referencing-0.37.0 rpds-py-2026.9.1 ruamel.yaml-0.19.1 shopsystem-kb-0.9.0 six-1.17.0 typing-extensions-4.16.0

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: python3 -m pip install --upgrade pip
~~~~~~
