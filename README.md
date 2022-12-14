# PipeDreams
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193423638-1d37a040-c230-48b5-a7dc-78e5a56ed3e2.gif" width="25%">
</p>

- This is an ongoing personal project for myself, for my team, i work on this after hours in my freetime, so it has been a slow but fun process so far trying to figure out
  how to build a animation VFX Pipeline!

- Looking at doing a major rebuild/restructure soon.

- Currently, PipeDreams is a basic Pipeline (mostly a DCC launcher for now) 
  that allows a small team of 3D artists to work seemlessly together on the same projects,
  it modifies the 3D package to a specific project environment, provides core tools for the DCC, such as a Scene Manager, Export Manager and a Capture Manager,
  these set of tools allows for the automotation of repetitive importing and exporting of assets, while keeping the file structure and naming conventions neat
  with versioning control.

- Users can choose and save custom icons and minimize the tool, alternatively this feature can be overridden by admin and force a companies logo instead.
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193425250-52573a42-4f55-4e63-855e-97dcd30b9956.gif" align="center" width="60%">
</p>

- SetShots and launch DCC. (ugly UI i know, but wipwip!)
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193425662-2d312af8-2142-4f1c-a282-e8f70ff68dc4.gif" align="center" width="60%">
</p>

- Maya drop down menu to PDS tools. alternatively top drop down menu title can be renamed to company name. in the config settings.
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193426682-070255d3-cdab-4733-bc82-0139f16ca850.png" align="center" width="50%">
</p>

- Optional toolBar instead of the above dropdown menu, it includes a quicksave with a specific naming convention / versioning to the specific show / shot. 
  which would hopefully encourage consistant naming accross all projects and shot, wip!
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/196048340-bc0a005d-658b-49cd-ab57-40ad49d97026.gif" align="center" width="100%">
</p>

- Maya Scene Manager, to import assets for specific project / show.
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193425740-a93b7e42-1467-4a72-98df-f40bcb2f3599.gif" align="center" width="80%">
</p>

- Maya Export Manager for specific shots and user scene, with the ability to delete from the check list and change an assets settings before exporting.
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193425846-dcd8e877-34ac-49a1-a287-d29e353c79a5.png" align="center" width="80%">
</p>

- Capture Manager.
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193425987-bd7f166e-942d-44f7-be23-cd48d6bbce04.png" align="center" width="30%">
</p>

- Capture Manager goes through a compositing process to format a version of a capture for dailies, it collect scene data and displays it in this capture too along with
  company logo, ideally this capture would be used by Ftrack etc, unfortunatly i dont have access to Ftrack to be able to implement it.
<p align="center">
<img src="https://user-images.githubusercontent.com/80905013/193426188-cf7f21fd-d2cb-4a62-850c-f8366a01eba3.gif" align="center" width="100%">
</p>

There are 2 versions of the pipeline for the DCC apps within this system, a development version and a production version, with its own very basic version control,
This would allow Pipeline TDS to continue building DCC tools in dev mode and later pushing it to productions (which is the version the artists use, this helps avoid, breaking the tools and affecting their workflow. i dont really know what is the best way to go about this, but this is the way i decided to build it.)

All these tools are in a very rough state, and needs loads of love and work! and probably very dirty code, but the more i learn, the more i try to rebuild and improve it. =)



