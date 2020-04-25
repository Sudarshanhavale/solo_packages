# solo_packages

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Packages](#Packages)

## General info
This Project contains helpful production tools for the Vfx Artists.  
	
## Technologies
* Python version: 2.7
	
## Packages
* **List Special:** 
Returns unique file patterns and details in structured format.
Its helps many departments like ingestion, dmp, lighting, compositing 
to understand and verify their files/sequences. eg: Lighting and 
compositers could be able to find missing frames easily and 
ingestion team would be able to find out patterns out of massive 
files data they receive from client. 
Here is a quick [demonstration](https://youtu.be/bqmVw71gWZQ "List Special") of visual understanding.   

* **Attribute Change Recorder:** 
This tool records attribute changes happening in the selected 
object and apply the same on multiple selections. Usually, 
Maya provides preset a mechanism which works on all attributes 
of selected objects. But if the one wants to change a certain 
set of attributes then it is bit manual work even if you use 
spreadsheets. This tool allows to record number of actions a user 
is doing on selected attribute and apply them on any given selections. 
It also identifies the same node types from given selections to 
apply changes on. So it becomes quite hassle-free for the artists 
to use. This is mainly useful for rigging, animation, layout, 
environment, and lighting as they play a lot with a set of 
attributes on a daily bases.
Here is a quick [demonstration](https://youtu.be/oN4bzeRd7xY "AttributeChangeRecorder") for visual understanding.

* **SnowBuilder Tool:**
This Snow setup tool helps CG artists to procedurally built 
a snow surface around complex shapes in very less amount of time. 
This also allows artists to procedurally generate different Snow 
Surface varieties in the same setup/file. Artist can bake/store 
their shortlisted outputs and choose a final one at any point 
of time without affecting any of his other output. 
Artists can apply his favorite output on any other object 
to get a similar look. In the given [demonstration](https://youtu.be/bcltw87ySDg "Snow Builder") I have 
generated approximately 5 to 10 different snow varieties on 
complex objects nearly in 10 mins.


