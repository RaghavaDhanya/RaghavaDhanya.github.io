---
title: "Python With a Dash of C++: Optimizing Recommendation Serving"
date: 2022-06-30T16:54:09+05:30
draft: true
cover:
    image: /images/python-with-a-dash-of-cpp-optimizing/cpp_python1.png
    caption: "Python on C++ Illustration"
    alt: A blue and yellow python wrapped around C++ logo
---
Serving recommendation to 200+ millions of users for thousands of candidates with less than 100ms is **hard** but doing that in python is **harder**. Why not add some compiled spice to it to make it faster? Using cython you can add C++ components to your python code. Isn't all machine learning and statistics library already written in C and Cython to make the super fast? Yes. But there's still some optimizations left on the table. I'll go through how we optimized some of our sampling methods in recommendation system using C++. 


Multi Armed Bandit(MAB) is one of the simpler model in our arsenal, this generally comes down to sampling from Beta distribution or an related distributions using specific distribution parameters for each user and candidate. So recommending for a user is mostly sampling thousands of times from thousands of distribution with different parameters.

