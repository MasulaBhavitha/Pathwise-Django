"""Catalog content for the student skill and career roadmap."""

CATEGORIES = [
    {
        "name": "Programming",
        "slug": "programming",
        "sort_order": 1,
        "description": "Languages and the habits that make code trustworthy.",
    },
    {
        "name": "Web",
        "slug": "web",
        "sort_order": 2,
        "description": "Interfaces, APIs, and the glue between them.",
    },
    {
        "name": "Data",
        "slug": "data",
        "sort_order": 3,
        "description": "Questions, evidence, and the tools that turn tables into decisions.",
    },
    {
        "name": "Cloud and systems",
        "slug": "cloud-systems",
        "sort_order": 4,
        "description": "How software runs, ships, and stays up.",
    },
    {
        "name": "Design",
        "slug": "design",
        "sort_order": 5,
        "description": "Research and craft for products people can actually use.",
    },
    {
        "name": "Professional",
        "slug": "professional",
        "sort_order": 6,
        "description": "The skills that make technical work land with a team.",
    },
]

SKILLS = [
    ("programming", "python", "Python", "Readable scripts, data work, and backend services."),
    ("programming", "javascript", "JavaScript", "The language of the browser and many APIs."),
    ("programming", "sql", "SQL", "Ask precise questions of relational data."),
    ("programming", "java", "Java", "Typed application code used across large systems."),
    ("programming", "git", "Git", "History, branches, and reviewable changes."),
    ("web", "html-css", "HTML & CSS", "Semantic pages, layout, and responsive design."),
    ("web", "react", "React", "Component interfaces with state and composition."),
    ("web", "rest-apis", "REST APIs", "Design, call, and document HTTP interfaces."),
    ("web", "nodejs", "Node.js", "JavaScript on the server and in build tools."),
    ("web", "testing", "Testing", "Automated checks that protect a change."),
    ("data", "statistics", "Statistics", "Uncertainty, distributions, and honest claims."),
    ("data", "data-visualization", "Data visualization", "Charts that answer a question at a glance."),
    ("data", "pandas", "Pandas", "Clean and reshape tabular data in Python."),
    ("data", "machine-learning", "Machine learning", "Train, evaluate, and explain predictive models."),
    ("data", "excel", "Spreadsheets", "Cleaning, pivots, and quick analysis."),
    ("cloud-systems", "linux", "Linux", "Shell, processes, files, and logs."),
    ("cloud-systems", "docker", "Docker", "Package an app so it runs the same everywhere."),
    ("cloud-systems", "ci-cd", "CI/CD", "Automate test and release on every change."),
    ("cloud-systems", "cloud-fundamentals", "Cloud fundamentals", "Compute, storage, and regions on a public cloud."),
    ("cloud-systems", "networking", "Networking", "DNS, ports, HTTP, and how requests travel."),
    ("design", "ux-research", "UX research", "Interviews, notes, and evidence about users."),
    ("design", "visual-design", "Visual design", "Hierarchy, type, color, and spacing."),
    ("design", "figma", "Figma", "Flows, components, and prototypes."),
    ("design", "accessibility", "Accessibility", "Interfaces that work with keyboard, screen readers, and contrast."),
    ("professional", "communication", "Communication", "Writing and speaking so other people can act."),
    ("professional", "problem-solving", "Problem solving", "Frame the question before picking a solution."),
    ("professional", "agile", "Agile teamwork", "Small increments, feedback, and shared plans."),
    ("professional", "technical-writing", "Technical writing", "READMEs, briefs, and docs people finish."),
]


def step(title, detail, skill="", label="", url=""):
    return {
        "title": title,
        "detail": detail,
        "skill": skill or None,
        "resource_label": label,
        "resource_url": url,
    }


CAREERS = [
    {
        "title": "Frontend Engineer",
        "slug": "frontend-engineer",
        "summary": "Build the interfaces students and customers actually touch.",
        "description": (
            "Frontend engineers turn product intent into fast, accessible interfaces. "
            "The work mixes visual craft, JavaScript, and collaboration with design and API teams. "
            "A strong student portfolio shows shipped screens, not only tutorials."
        ),
        "outlook": "High demand",
        "salary_range": "$85k–$150k",
        "accent": "#c45c26",
        "requirements": [
            ("html-css", 4, "core"),
            ("javascript", 4, "core"),
            ("react", 4, "core"),
            ("git", 3, "core"),
            ("rest-apis", 3, "core"),
            ("accessibility", 3, "core"),
            ("testing", 3, "recommended"),
            ("nodejs", 2, "recommended"),
            ("communication", 3, "recommended"),
        ],
        "stages": [
            {
                "title": "Web foundations",
                "summary": "Pages that are semantic, responsive, and readable.",
                "weeks": 4,
                "steps": [
                    step(
                        "Ship a personal page",
                        "Publish a one-page site about you, with real content, a mobile layout, and no framework.",
                        "html-css",
                        "MDN HTML",
                        "https://developer.mozilla.org/en-US/docs/Web/HTML",
                    ),
                    step(
                        "Rebuild a screen from a screenshot",
                        "Match spacing and type with flexbox and grid. Write down what you had to approximate.",
                        "html-css",
                        "MDN CSS layout",
                        "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout",
                    ),
                    step(
                        "Fix the accessibility basics",
                        "Add headings, labels, focus states, and color contrast that passes a checker.",
                        "accessibility",
                        "MDN accessibility",
                        "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility",
                    ),
                ],
            },
            {
                "title": "JavaScript fluency",
                "summary": "Behavior you can explain without a library.",
                "weeks": 5,
                "steps": [
                    step(
                        "Drill the language core",
                        "Practice types, functions, arrays, objects, and asynchronous code until small katas feel routine.",
                        "javascript",
                        "javascript.info",
                        "https://javascript.info/",
                    ),
                    step(
                        "Build a quiz without a framework",
                        "State, events, and rendering live in a few modules. Handle an empty question list.",
                        "javascript",
                    ),
                    step(
                        "Read and show remote data",
                        "Fetch a public API, show a loading state, and explain the failure when the network drops.",
                        "rest-apis",
                        "MDN Fetch",
                        "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch",
                    ),
                ],
            },
            {
                "title": "React interface",
                "summary": "Components with state, routing, and a test.",
                "weeks": 5,
                "steps": [
                    step(
                        "Rebuild the quiz in React",
                        "Split the UI into components. Keep state as local as it can be.",
                        "react",
                        "React quick start",
                        "https://react.dev/learn",
                    ),
                    step(
                        "Add routes and a form",
                        "One list view, one detail view, and a form that validates before it submits.",
                        "react",
                    ),
                    step(
                        "Test one component",
                        "Cover the happy path and one error path so a refactor cannot silently break it.",
                        "testing",
                        "React testing guide",
                        "https://react.dev/reference/react",
                    ),
                ],
            },
            {
                "title": "Portfolio and review",
                "summary": "Work other people can clone, run, and critique.",
                "weeks": 4,
                "steps": [
                    step(
                        "Publish with a clean Git history",
                        "Small commits, a README with setup steps, and a link someone else can open.",
                        "git",
                        "Git book",
                        "https://git-scm.com/book/en/v2",
                    ),
                    step(
                        "Give and receive a review",
                        "Review a classmate's pull request and revise yours from their notes.",
                        "communication",
                    ),
                    step(
                        "Write the case study",
                        "One page: the user, the constraint, the tradeoff, and what you would do next.",
                        "technical-writing",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Backend Engineer",
        "slug": "backend-engineer",
        "summary": "Design the services, data, and rules behind a product.",
        "description": (
            "Backend engineers model data, expose safe APIs, and keep behavior correct as it changes. "
            "Students heading here should be comfortable with one language, SQL, and automated tests."
        ),
        "outlook": "High demand",
        "salary_range": "$90k–$160k",
        "accent": "#1f6b5a",
        "requirements": [
            ("python", 4, "core"),
            ("sql", 4, "core"),
            ("rest-apis", 4, "core"),
            ("git", 3, "core"),
            ("testing", 3, "core"),
            ("docker", 3, "recommended"),
            ("linux", 3, "recommended"),
            ("java", 2, "recommended"),
            ("technical-writing", 3, "recommended"),
        ],
        "stages": [
            {
                "title": "Python craft",
                "summary": "Small programs with tests and clear boundaries.",
                "weeks": 4,
                "steps": [
                    step(
                        "Write functions and modules",
                        "Solve three small problems as importable functions, not one long script.",
                        "python",
                        "Python tutorial",
                        "https://docs.python.org/3/tutorial/",
                    ),
                    step(
                        "Model a tiny domain",
                        "Represent students, skills, and enrollments with dataclasses or classes.",
                        "python",
                    ),
                    step(
                        "Test the edges",
                        "Empty input, duplicates, and a bad id each get a test with a clear name.",
                        "testing",
                    ),
                ],
            },
            {
                "title": "Data and APIs",
                "summary": "Tables and HTTP that match the product language.",
                "weeks": 5,
                "steps": [
                    step(
                        "Design tables and write joins",
                        "Sketch a schema on paper, then query it with filters, aggregates, and one join.",
                        "sql",
                        "PostgreSQL tutorial",
                        "https://www.postgresql.org/docs/current/tutorial.html",
                    ),
                    step(
                        "Build a REST API",
                        "List, create, and update one resource. Reject invalid input with a useful error.",
                        "rest-apis",
                    ),
                    step(
                        "Document the contract",
                        "Write the endpoints, fields, and error shapes a frontend partner would need.",
                        "technical-writing",
                    ),
                ],
            },
            {
                "title": "Run it somewhere",
                "summary": "A service you can start, log, and rebuild.",
                "weeks": 4,
                "steps": [
                    step(
                        "Containerize the API",
                        "A Dockerfile and a short note on how to build and run it.",
                        "docker",
                        "Docker getting started",
                        "https://docs.docker.com/get-started/",
                    ),
                    step(
                        "Read logs on Linux",
                        "Start the app in a terminal, trigger an error, and find the line that explains it.",
                        "linux",
                    ),
                    step(
                        "Run tests in CI",
                        "Every push runs the test command and fails the check when tests fail.",
                        "ci-cd",
                        "GitHub Actions",
                        "https://docs.github.com/en/actions/get-started",
                    ),
                ],
            },
            {
                "title": "A feature with a reason",
                "summary": "Ship one change you can defend.",
                "weeks": 3,
                "steps": [
                    step(
                        "Frame the problem first",
                        "Write the user need in one paragraph before you open the editor.",
                        "problem-solving",
                    ),
                    step(
                        "Ship the change with Git",
                        "Branch, commit, and open a pull request that says what changed and why.",
                        "git",
                        "Git book",
                        "https://git-scm.com/book/en/v2",
                    ),
                    step(
                        "Explain it out loud",
                        "Walk a classmate through the request flow in under five minutes.",
                        "communication",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Data Analyst",
        "slug": "data-analyst",
        "summary": "Turn messy records into a recommendation someone can use.",
        "description": (
            "Data analysts spend more time defining the question than picking a chart. "
            "SQL, spreadsheets, and a clear written conclusion matter more than a large model."
        ),
        "outlook": "Steady demand",
        "salary_range": "$70k–$120k",
        "accent": "#1e4d7b",
        "requirements": [
            ("sql", 4, "core"),
            ("excel", 4, "core"),
            ("statistics", 4, "core"),
            ("data-visualization", 4, "core"),
            ("communication", 4, "core"),
            ("python", 3, "recommended"),
            ("pandas", 3, "recommended"),
            ("problem-solving", 3, "recommended"),
        ],
        "stages": [
            {
                "title": "Spreadsheet thinking",
                "summary": "Clean data and a chart with a sentence underneath.",
                "weeks": 3,
                "steps": [
                    step(
                        "Clean a messy sheet",
                        "Fix types, blanks, and duplicates. Keep a note of every assumption.",
                        "excel",
                    ),
                    step(
                        "Answer with a pivot",
                        "One business question, one pivot, and the number you would quote in a meeting.",
                        "excel",
                    ),
                    step(
                        "Chart the comparison",
                        "Choose a chart that fits the question. Title it with the finding, not the chart type.",
                        "data-visualization",
                    ),
                ],
            },
            {
                "title": "SQL for questions",
                "summary": "The same questions, asked of a database.",
                "weeks": 4,
                "steps": [
                    step(
                        "Filter and aggregate",
                        "Write selects that count, average, and group. Name the columns in plain language.",
                        "sql",
                        "PostgreSQL tutorial",
                        "https://www.postgresql.org/docs/current/tutorial.html",
                    ),
                    step(
                        "Join two tables",
                        "Combine entities without double-counting. Say what the join key is.",
                        "sql",
                    ),
                    step(
                        "Write the question first",
                        "A half-page brief: decision, metric, grain, and what would change your mind.",
                        "problem-solving",
                    ),
                ],
            },
            {
                "title": "Python analysis",
                "summary": "A notebook someone else can rerun.",
                "weeks": 4,
                "steps": [
                    step(
                        "Clean with Pandas",
                        "Load a CSV, handle missing values, and save the tidy table.",
                        "pandas",
                        "Pandas getting started",
                        "https://pandas.pydata.org/docs/getting_started/index.html",
                    ),
                    step(
                        "Describe the uncertainty",
                        "Mean, spread, and a sentence about what you cannot claim from this sample.",
                        "statistics",
                    ),
                    step(
                        "Repeat the spreadsheet story",
                        "Reach the same conclusion in code and note where the numbers differ.",
                        "python",
                        "Python tutorial",
                        "https://docs.python.org/3/tutorial/",
                    ),
                ],
            },
            {
                "title": "Decision memo",
                "summary": "A recommendation, not a pile of charts.",
                "weeks": 3,
                "steps": [
                    step(
                        "Compare two options",
                        "Recommend one, with the metric, the tradeoff, and the risk.",
                        "problem-solving",
                    ),
                    step(
                        "Publish the narrative",
                        "A short memo or notebook: question, method, result, next step.",
                        "technical-writing",
                    ),
                    step(
                        "Present in five minutes",
                        "Practice once out loud. Cut any chart that does not support the ask.",
                        "communication",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Machine Learning Engineer",
        "slug": "machine-learning-engineer",
        "summary": "Train models that can be evaluated, explained, and rerun.",
        "description": (
            "This path is for students who like both modeling and software. "
            "A baseline you can measure beats a complex model you cannot reproduce."
        ),
        "outlook": "High demand",
        "salary_range": "$110k–$180k",
        "accent": "#7a3e55",
        "requirements": [
            ("python", 5, "core"),
            ("machine-learning", 4, "core"),
            ("statistics", 4, "core"),
            ("pandas", 4, "core"),
            ("sql", 3, "core"),
            ("git", 3, "core"),
            ("docker", 3, "recommended"),
            ("cloud-fundamentals", 3, "recommended"),
            ("problem-solving", 4, "recommended"),
        ],
        "stages": [
            {
                "title": "Foundations",
                "summary": "Python, tables, and the statistics you will quote.",
                "weeks": 5,
                "steps": [
                    step(
                        "Refresh probability",
                        "Explain mean, variance, and a train/test split without slides full of formulas.",
                        "statistics",
                    ),
                    step(
                        "Get fluent in Python",
                        "Functions, files, and virtual environments. No notebook-only workflow.",
                        "python",
                        "Python tutorial",
                        "https://docs.python.org/3/tutorial/",
                    ),
                    step(
                        "Build a feature table",
                        "Use Pandas to produce one row per example and write down each column.",
                        "pandas",
                        "Pandas getting started",
                        "https://pandas.pydata.org/docs/getting_started/index.html",
                    ),
                ],
            },
            {
                "title": "A measurable baseline",
                "summary": "The smallest model that can be wrong in public.",
                "weeks": 5,
                "steps": [
                    step(
                        "Train a baseline",
                        "Fit a simple model. Record the metric before you try anything clever.",
                        "machine-learning",
                        "scikit-learn",
                        "https://scikit-learn.org/stable/getting_started.html",
                    ),
                    step(
                        "Check for leakage",
                        "Confirm the test set never shaped the features. Write the split rule down.",
                        "machine-learning",
                    ),
                    step(
                        "Explain the errors",
                        "Look at ten mistakes and say what they have in common.",
                        "communication",
                    ),
                ],
            },
            {
                "title": "Make it repeatable",
                "summary": "Someone else can train what you trained.",
                "weeks": 4,
                "steps": [
                    step(
                        "Put the data query in SQL",
                        "The training set comes from a query you can rerun, not a mystery export.",
                        "sql",
                        "PostgreSQL tutorial",
                        "https://www.postgresql.org/docs/current/tutorial.html",
                    ),
                    step(
                        "Version the training script",
                        "Git history shows the metric before and after a change.",
                        "git",
                        "Git book",
                        "https://git-scm.com/book/en/v2",
                    ),
                    step(
                        "Containerize training or inference",
                        "One command reproduces the environment.",
                        "docker",
                        "Docker getting started",
                        "https://docs.docker.com/get-started/",
                    ),
                ],
            },
            {
                "title": "Hand it to a product",
                "summary": "A prediction with a written limit.",
                "weeks": 4,
                "steps": [
                    step(
                        "Serve one prediction",
                        "A small HTTP endpoint accepts input and returns a score plus a version.",
                        "rest-apis",
                    ),
                    step(
                        "Sketch the cloud path",
                        "Name where the data lives, where training runs, and what this would cost to try.",
                        "cloud-fundamentals",
                        "AWS overview",
                        "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html",
                    ),
                    step(
                        "Write a model card",
                        "Purpose, data, metric, and the cases where the model should not be used.",
                        "technical-writing",
                    ),
                ],
            },
        ],
    },
    {
        "title": "UI/UX Designer",
        "slug": "ui-ux-designer",
        "summary": "Study a task, then shape an interface people can finish.",
        "description": (
            "Design students on this path practice research, visual hierarchy, and a prototype of one real task. "
            "A case study with evidence is the portfolio piece employers remember."
        ),
        "outlook": "Steady demand",
        "salary_range": "$75k–$130k",
        "accent": "#8c4a1f",
        "requirements": [
            ("ux-research", 4, "core"),
            ("visual-design", 4, "core"),
            ("figma", 4, "core"),
            ("accessibility", 4, "core"),
            ("communication", 4, "core"),
            ("html-css", 3, "recommended"),
            ("problem-solving", 3, "recommended"),
            ("agile", 2, "recommended"),
        ],
        "stages": [
            {
                "title": "See the user",
                "summary": "Evidence before pixels.",
                "weeks": 3,
                "steps": [
                    step(
                        "Interview two people",
                        "Ask about a recent task. Capture quotes, not your solution ideas.",
                        "ux-research",
                    ),
                    step(
                        "Write the problem statement",
                        "Who, what they are trying to do, and what gets in the way. No UI yet.",
                        "problem-solving",
                    ),
                    step(
                        "Map the current journey",
                        "Steps, tools, and the moment they stall.",
                        "ux-research",
                    ),
                ],
            },
            {
                "title": "Shape the interface",
                "summary": "Structure, then visual design.",
                "weeks": 4,
                "steps": [
                    step(
                        "Sketch the flow in Figma",
                        "Low-fidelity screens for the core task only.",
                        "figma",
                        "Figma design basics",
                        "https://help.figma.com/hc/en-us/articles/360041061214-Design-basics",
                    ),
                    step(
                        "Set type, color, and spacing",
                        "A small system: two type sizes that matter, one accent, consistent spacing.",
                        "visual-design",
                    ),
                    step(
                        "Check access",
                        "Contrast, labels, and a keyboard path through the main task.",
                        "accessibility",
                        "MDN accessibility",
                        "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility",
                    ),
                ],
            },
            {
                "title": "Make it feel real",
                "summary": "A prototype and a slice of the UI in the browser.",
                "weeks": 4,
                "steps": [
                    step(
                        "Prototype the core task",
                        "Clickable enough that a classmate can finish the task without your narration.",
                        "figma",
                    ),
                    step(
                        "Build one screen in HTML and CSS",
                        "So you can talk with engineers about what is hard.",
                        "html-css",
                        "MDN CSS layout",
                        "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout",
                    ),
                    step(
                        "Revise from a critique",
                        "Ask one hard question, change the design, and note what you refused to change.",
                        "communication",
                    ),
                ],
            },
            {
                "title": "Case study",
                "summary": "The story of the decision, not a gallery.",
                "weeks": 3,
                "steps": [
                    step(
                        "Write the case study",
                        "Research, options, the decision, and the outcome or the open risk.",
                        "technical-writing",
                    ),
                    step(
                        "Present it in eight beats",
                        "Problem, evidence, concept, critique, revision, access, next step, ask.",
                        "communication",
                    ),
                    step(
                        "Plan the next increment",
                        "A short backlog a teammate could pick up next week.",
                        "agile",
                    ),
                ],
            },
        ],
    },
    {
        "title": "DevOps Engineer",
        "slug": "devops-engineer",
        "summary": "Make build, release, and recovery boring in the best way.",
        "description": (
            "DevOps work is the path from a laptop demo to a service other people can trust. "
            "Linux, containers, and a pipeline you have broken and fixed are the proof."
        ),
        "outlook": "High demand",
        "salary_range": "$95k–$165k",
        "accent": "#3f5c3a",
        "requirements": [
            ("linux", 4, "core"),
            ("docker", 4, "core"),
            ("ci-cd", 4, "core"),
            ("cloud-fundamentals", 4, "core"),
            ("git", 4, "core"),
            ("networking", 3, "core"),
            ("python", 3, "recommended"),
            ("testing", 3, "recommended"),
            ("technical-writing", 3, "recommended"),
        ],
        "stages": [
            {
                "title": "The machine",
                "summary": "Comfortable in a shell and on the network.",
                "weeks": 4,
                "steps": [
                    step(
                        "Live in the shell",
                        "Files, permissions, processes, and a command you can explain line by line.",
                        "linux",
                    ),
                    step(
                        "Trace one request",
                        "DNS, port, and HTTP status for a site you use. Draw the path.",
                        "networking",
                    ),
                    step(
                        "Automate a chore",
                        "A short Python or shell script that replaces a manual setup step.",
                        "python",
                        "Python tutorial",
                        "https://docs.python.org/3/tutorial/",
                    ),
                ],
            },
            {
                "title": "Build and ship",
                "summary": "The artifact and the pipeline that produces it.",
                "weeks": 4,
                "steps": [
                    step(
                        "Practice a branching habit",
                        "Feature branch, review, and a history you would not be embarrassed to show.",
                        "git",
                        "Git book",
                        "https://git-scm.com/book/en/v2",
                    ),
                    step(
                        "Write a Dockerfile",
                        "Build an image, run it, and change one line to prove you understand the cache.",
                        "docker",
                        "Docker getting started",
                        "https://docs.docker.com/get-started/",
                    ),
                    step(
                        "Add a pipeline",
                        "Push to a branch, run tests, and publish the result or fail loudly.",
                        "ci-cd",
                        "GitHub Actions",
                        "https://docs.github.com/en/actions/get-started",
                    ),
                ],
            },
            {
                "title": "A small cloud footprint",
                "summary": "Something running that is not your laptop.",
                "weeks": 4,
                "steps": [
                    step(
                        "Name the cloud pieces",
                        "Compute, storage, and network for a tiny app. Estimate a student-budget cost.",
                        "cloud-fundamentals",
                        "AWS overview",
                        "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html",
                    ),
                    step(
                        "Deploy the container",
                        "It stays up after you close the laptop. Record the exact commands.",
                        "docker",
                    ),
                    step(
                        "Add a health check",
                        "A failing process becomes a visible signal, not a surprise.",
                        "linux",
                    ),
                ],
            },
            {
                "title": "Operate it",
                "summary": "The notes you wish you had at 2 a.m.",
                "weeks": 3,
                "steps": [
                    step(
                        "Write a one-page runbook",
                        "How to tell it is down, the first three checks, and who to tell.",
                        "technical-writing",
                    ),
                    step(
                        "Add a test that would have caught a bad release",
                        "A check in the pipeline for a failure you actually hit.",
                        "testing",
                    ),
                    step(
                        "Walk someone through the release",
                        "They can repeat it from your notes without you typing.",
                        "communication",
                    ),
                ],
            },
        ],
    },
]
