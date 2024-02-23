---
title: "Showcase: BPMN Pipeline Platform"
date: 2022-06-20T20:54:07+05:30
lastmod:  2022-06-25T15:14:00+05:30
tags: ["mlops", "pipeline", "bpmn", "python", "r", "java", "ml", "ai"]
categories:
    - projects
    - musigma-labs
cover:
    image: /images/bpmn-pipeline-platform/cover.png
    caption: "A human in the loop pipeline"
    alt: "A BPMN pipeline containing tasks 'fetch data', 'load data & train model', 'approval from owner', 'deploy model' and 'email on failure to fetch data'. All script tasks are python"
---
At [Mu Sigma Labs](https://www.mu-sigma.com/labs), I led a significant project focused on BPMN-based analytics automation and pipeline orchestration. Using the open-source platform [Activiti](https://www.activiti.org/), I owned, developed, tested, and maintained a system serving about _3,000_ internal users, handling _critical_ reporting and data pipelines.

 
### Technologies Used
The core technologies employed were:

- Backend: Java and Spring Boot
- Scripting: Python and R for analytics tasks
- Frontend: Angular for user interface


## Understanding BPMN
[Business Process Model and Notation (BPMN)]((https://en.wikipedia.org/wiki/Business_Process_Model_and_Notation)) provided the foundation for our automation approach. BPMN, a graphical notation standard for business processes, was extended to accommodate automated pipelines and human-in-the-loop processes.

A simple example:
![flow that takes input file and mails](/images/bpmn-pipeline-platform/simple-example.png)

Two major extensions were made by us to the platform:

### Scripting tasks: Key to Automation
We integrated R and Python scripting into the platform to enable sophisticated automation tasks. This capability allowed us to design complex pipelines like propensity-to-click prediction model involving user input, predictive modeling, and approval workflows. Example:
![A propensity to click prediction flow](/images/bpmn-pipeline-platform/flow-example-1.png)


### User tasks: Human in the loop
User tasks, including forms and approvals, were seamlessly integrated with email notifications and the assigned user can use the link in the email to submit form or approve the task. This notification could include some context from the previous tasks by attaching documents. 
![A human in the loop pipeline](/images/bpmn-pipeline-platform/cover.png)

### Pure Pipelining Example
You can also use it as simple pipelining by chaining just scripting tasks.

Example: 
![A scraping pipeline with just scripting and email tasks](/images/bpmn-pipeline-platform/pipeline-example.png)

### Dynamic Triggers
Our platform supported diverse trigger mechanisms, including cron-based schedules and REST APIs, ensuring seamless integration with external systems for task initiation.

## The Role of BPMN in ML pipelining?
Why use BPMN for automating / pipelining? We don't use [UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language) for coding right?

BPMN's adoption for automation and pipelining stemmed from its ability to cater to both technical and non-technical users. Whether orchestrating simple data flows or complex machine learning pipelines, BPMN empowered users to architect automated workflows with ease and flexibility.

Moreover, platforms's support for human-in-the-loop processes addressed a critical gap in conventional pipelining systems, offering robust mechanisms for human validation and approval—a necessity in the realm of machine learning and MLOps where human intervention is often required.

## Key Contributions
During my tenure, I focused on:
- Enabling scripting support for R and Python
- Enhancing Logging and Observability of these tasks. 
- Implementing timer and dynamic events. 
- Implementing dynamic user task assignments.
- Improving scalability and modularity of the platform
- Addressing user interface enhancements and optimizations

## Recognition ⭐️
For my contributions, I received a spot award.
![spot award](/images/bpmn-pipeline-platform/spot_award_2.png) 



