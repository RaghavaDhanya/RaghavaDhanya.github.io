---
title: "BPMN Pipeline Platform"
date: 2022-06-20T20:54:07+05:30
draft: true
tags: ["mlops", "pipeline", "bpmn", "python", "r", "java"]
categories:
    - projects
---
One of my major work at [Mu Sigma Labs](https://www.mu-sigma.com/our-platform/business-intelligence-services-innovation-lab) was with BPMN based analytics automation/ pipeline platform. Based on an open source platform [Activiti](https://www.activiti.org/). I was the owner and developed, tested, maintained the platform. 
It served about **3k** internal users and ran several **critical** reporting and data pipelines.
 
### Technologies Used
`Java`, `Spring Boot` as Backend. The platform itself supported scripting in `Python`, `R` for automation. `Angular` for Frontend.


## BPMN
Business Process Model and Notation (BPMN) is a standard for modeling business processes in a graphical notation. Read more [here](https://en.wikipedia.org/wiki/Business_Process_Model_and_Notation). Classically this is only used for describing Business Processes but with scripting tasks, We can easily extend this to automated pipelines and human in the loop pipelines.

A simple example:
![flow that takes input file and mails](/images/bpmn-pipeline-platform/simple-example.png)

### Scripting tasks
I was involved in making the platform support R and Python for scripting automations. With scripting we could make complicated pipelines such as 
![A propensity to click prediction flow](/images/bpmn-pipeline-platform/flow-example-1.png)
This pipeline involves user forms, model prediction and approval. You can imagine extending this flow to retraining and approval of said retrained model based on metrics.

### User tasks
User tasks such as forms and approval are sent as email and the assigned user can use the link in the email to submit form or approve the task. You can even attach documents to the email component from previous tasks for more context on approval.

### Using for Simple Pipelining
You can also use it as simple pipelining by chaining just scripting tasks.

Example: 
![A scraping pipeline with just scripting and email tasks](/images/bpmn-pipeline-platform/pipeline-example.png)

### Triggers
The flow could be triggered by a schedule based on cron expression or it could be triggered using a REST API. The REST API were used by other products and platform to trigger their flow to send user reports, stress test reports etc.

## Why?
Why use BPMN for automating / pipelining? We don't use [UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language) for coding right?

One of the aims of the platform is to support both technical and non technical users, You want a simple flow to take input from many users and mail it to you? you can just do that with no code. You want to scrape data, train model, calculate metrics and ask you if it should be deployed and deploy? Can do.

Another important feature that many pipelining systems seem to lack is human in the loop pipelines. There are lots of cases in Machine Learning and MLOps where you would need to verify with a human or get approval before you do something like deployment. BPMN has notation and components to support this use-case, why not use them.

## My work
My major work was in 
- supporting R and Python in scripting tasks,
- Logging and debug-ability of these tasks. 
- Supporting complicated timer and other events in the flow and dynamic events. 
- Dynamic User task assignments.
- Making it scalable and modular overall
- Small UI fixes

## Award ⭐️
I was awarded a [spot award](/images/bpmn-pipeline-platform/spot_award_2.jpg) for my work on this



