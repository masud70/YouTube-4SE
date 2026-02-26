instructions = {
    "role": "system",
    "content": "You are a strict binary classifier for Software Engineering educational content.\n\nDefinition of Software Engineering educational content:\nSoftware Engineering YouTube videos that contribute to Software Engineering (SE) education worldwide, grounded in the knowledge areas defined by the SWEBOK Guide V4.0a. Software Engineering is defined as the systematic, disciplined, and measurable approach to the specification, design, construction, testing, deployment, operation, maintenance, management, and evolution of software systems. The scope includes content aligned with SWEBOK knowledge areas such as Software Requirements, Architecture, Design, Construction, Testing, Maintenance, Configuration Management, Engineering Operations (including DevOps and release engineering), Software Engineering Management, Process, Models and Methods, Software Quality, Software Security, Professional Practice, and Software Engineering Economics. It also includes research-oriented topics—such as empirical software engineering, software metrics, AI for software engineering, secure development life cycles, and process improvement—when they directly relate to improving software systems or engineering practices. Foundational topics from Computing, Mathematical, and Engineering Foundations are included only when presented in support of software engineering activities (e.g., algorithms for software performance, AI in SE, networking for distributed systems). Content related to software product strategy, release planning, SaaS engineering models, and economic decision-making is included when explicitly tied to the software lifecycle. Excluded are videos focused solely on hardware engineering, general computer science theory without connection to software engineering practice, pure programming syntax tutorials without engineering context, general technology news, or business topics unrelated to software system development and management.\n\nTask:\nGiven the TITLE and DESCRIPTION of a YouTube video, determine whether the video is related to Software Engineering education.\n\nInput:\nTITLE: {title}\nDESCRIPTION: {description}\n\nOutput rules\n- Do NOT explain, output anything else, add punctuation, or add additional words with your answer.\n- Respond with ONLY one word: True if related or False if not related."
}

examples = [
    [
        {
            "role": "user",
            "content": "TITLE: What is RTM in Testing || Manual Testing full course #34 || Software Testing with Sumit, DESCRIPTION: What is RTM document in the software testing process. What is BRS, SRS , FRS & FNRS. What is test suite. Explanation how to work RTM documents. What is Test Plan & FRD."
        },
        {
            "role": "assistant",
            "content": "True"
        }
    ],
    [
        {
            "role": "user",
            "content": "TITLE: The United Architects of the Philippines (UAP) National Headquarters Building @arki-knows, DESCRIPTION: The United Architects of the Philippines (UAP) National Headquarters Building was Inaugurated on June 6,2002. \n\nAn obra of Ar. Teofilo I.Vasquez,fuap,apec architect,asean architect as its Architect-Of-Record.\n\nUnveiled on October 2nd, 2020 on the occasion of his 62nd birth anniversary.\n\nThe Engineering Design Consultants are:\nStructural : GPE Resource Consultants\nSanitary : Anthony J.Lara and Associates\nElectrical : Cesar Tadeo and Associates\nMechanical : Trans-Asia (Phils) Inc.\nFire Protection : Oscar S. Roque and Associates"
        },
        {
            "role": "assistant",
            "content": "False"
        }
    ],
    [
        {
            "role": "user",
            "content": "TITLE: AI Coding Assistants: Tech Debt Factory or Friend? | Pallavi Deshpande, DESCRIPTION: Speed, fewer monotonous tasks, and improved developer flow are the promised  benefits.  The danger is that faster code leads to a quicker buildup of brittle, unsafe, and unmaintainable code. AI coding assistants promise increased productivity, but are we inadvertently building a mountain of tech debt? This talk will expose the hidden risks these tools introduce and equip you with practical strategies to mitigate them, ensuring your codebase remains robust and maintainable.\n\nAbout Pallavi Deshpande\n\nPallavi is a Technology leader with over 2 decades of experience in the digital industry. She has led global engineering teams through major transformations, building high-performing and innovative cultures along the way. A strong advocate of women in tech, Pallavi is deeply committed to driving diversity, inclusion, and meaningful change across the tech community."
        },
        {
            "role": "assistant",
            "content": "True"
        }
    ],
    [
        {
            "role": "user",
            "content": "TITLE: RubyConf 2017: Set Design: Putting the \"Art\" in \"Architecture\" by Betsy Haibel, DESCRIPTION: Set Design: Putting the \"Art\" in \"Architecture\" by Betsy Haibel\n\nI thought of software architects as petty waterfall dictators. Then I became one. My theater background saved me. In this talk, we\u2019ll look at set design \u2014 an ongoing, collaborative process \u2014 as a model for a more agile kind of \u201carchitecture\u201d than building metaphors allow us. You\u2019ll learn about the most important part of any architecture (hint: people), about using architecture to foster team creativity, and about the agile-architecture superpowers that Ruby gives us. No matter your title, you too can architect!"
        },
        {
            "role": "assistant",
            "content": "False"
        }
    ]
]

def get_messages(count: int = 0) -> list[dict[str, str]]:
    messages = [instructions]
    messages.extend(ex for example in examples[:count] for ex in example)
    return messages