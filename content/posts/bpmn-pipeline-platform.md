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

[Business Process Model and Notation (BPMN)](https://en.wikipedia.org/wiki/Business_Process_Model_and_Notation) is a graphical notation standard for business processes. Think of it as a flowchart for business processes. It is widely used in the industry for modeling business processes.
Now, why would you use BPMN for automating / pipelining? We don't use [UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language) for writing software right? Yes, but BPMN's adoption for automation and pipelining stemmed from its ability to cater to both technical and non-technical users. Whether orchestrating simple data flows or complex machine learning pipelines, BPMN empowered users to architect automated workflows with ease and flexibility. 
Moreover, platforms's support for human-in-the-loop processes addressed a critical gap in conventional pipelining systems, offering robust mechanisms for human validation and approval—a necessity in the realm of machine learning and MLOps where human intervention is often required.

A simple example:
![flow that takes input file and mails](/images/bpmn-pipeline-platform/simple-example.png)

In this post, I will showcase a BPMN-based analytics automation and pipeline orchestration platform that I led at [Mu Sigma Labs](https://www.mu-sigma.com/labs). The platform was used by about _3,000_ internal users, handling _critical_ reporting and data pipelines.

## The Challenge
The platform was designed to automate and orchestrate complex analytics workflows, including data pipelines, machine learning models, and human-in-the-loop processes. The key challenges were:
- **Scalability**: The platform needed to support thousands of users and hundreds of concurrent pipelines.
- **Flexibility**: The platform had to accommodate diverse use cases, from simple approval workflows to complex machine learning pipelines.
- **User Experience**: The platform had to be user-friendly, enabling both technical and non-technical users to design and execute workflows with ease.

## The Solution
We didn't have to start from scratch. We used [Activiti](https://www.activiti.org/), an open-source BPMN engine, as the core of the platform. Activiti provided a robust foundation, enabling us to focus on enhancing the platform's capabilities and user experience. We extended Activiti to support scripting tasks, human-in-the-loop processes, and dynamic triggers, enabling users to design and execute sophisticated analytics workflows with ease.

We used the following tech stack:
- **Backend**: Java, Activiti
- **Frontend**: Angular
- **Scripting**: R, Python
- **Database**: PostgreSQL

The major extensions we made to Activiti were:

### Scripting tasks: Key to Automation
We integrated R and Python scripting into the platform to enable sophisticated automation tasks. This capability allowed us to design complex pipelines like propensity-to-click prediction model involving user input, predictive modeling, and approval workflows. Example:
![A propensity to click prediction flow](/images/bpmn-pipeline-platform/flow-example-1.png)


### User tasks: Human in the loop
User tasks, including forms and approvals, were seamlessly integrated with email notifications and the assigned user can use the link in the email to submit form or approve the task. This notification could include some context from the previous tasks by attaching documents. 
![A human in the loop pipeline](/images/bpmn-pipeline-platform/cover.png)

### Dynamic Triggers
Our platform supported diverse trigger mechanisms, including cron-based schedules and REST APIs, ensuring seamless integration with external systems for task initiation.


## The Usecases

### Pure Pipelining Example
You can also use it as simple pipelining by chaining just scripting tasks.
Example: 
![A scraping pipeline with just scripting and email tasks](/images/bpmn-pipeline-platform/pipeline-example.png)

### Human in the loop
A human in the loop pipeline where the user has to approve the model before deploying it.
![A human in the loop pipeline](/images/bpmn-pipeline-platform/cover.png)


## My Key Contributions
During my tenure, I focused on:
- Enabling scripting support for R and Python
- Enhancing Logging and Observability of these tasks. 
- Implementing timer and dynamic events. 
- Implementing dynamic user task assignments.
- Improving scalability and modularity of the platform
- Addressing user interface enhancements and optimizations
- Building example models and pipelines to showcase the platform's capabilities.

## Recognition ⭐️
For my contributions, I received a spot award.
![spot award](/images/bpmn-pipeline-platform/spot_award_2.png) 



