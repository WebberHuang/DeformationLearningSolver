# Deformation Learning Solver for Autodesk Maya

Deformation Learning Solver is based on Smooth Skinning Decomposition with Rigid Bones which was an automated algorithm to extract the linear blend skinning (LBS) from a set of example poses, and made to convert any deformation approximation to joints and it's skinning-based. This allows there to be a savings in computing resources and a smaller data footprint.

This tool haven't be verified in real production yet, since this's just a personal research project to learn SSDR and skinning technique in deep, I don't have any plan for commercial release so far. 

Please feel free to test it at your own risk.

## Contact:
* Author: [Webber Huang](https://uk.linkedin.com/in/webber-huang-aab076100)
* Email: <xracz.fx@gmail.com>
* Project: [https://github.com/WebberHuang/DeformationLearningSolver](https://github.com/WebberHuang/DeformationLearningSolver)

## Demo: 
* [Deformation Learning Solver](https://vimeo.com/130998850)
* [Deformation Learning Solver v1.5](https://vimeo.com/138048608)

## Requires: 
Maya 2014 x64 and above, Windows, Linux and OS X

The solver has been compiled success on these platforms:

* Windows 7 64bit, Visual Studio 2013
* CentOS 7, GCC 4.8.3 with -std=c++11
* OS X 10.10, Xcode 6.1 with -std=gnu++0x

## Install:
* This tool is module based, you can place "DeformationLearningSolver" folder to any where.

* Launch maya, drag install.mel into scene, a new icon will be created in current shelf, launch Deformation Learning Solver by clicking the icon.

### Manual Install:
* What 'install.mel' does is to create 'DeformationLearningSolver.mod' in */YOUR/HOME/DIRECTORY/maya/modules* (ie. *C:/Users/YourName/Documents/maya/modules*), and setup the installation path, then maya will find this tool automatically. In the same way, you can put 'DeformationLearningSolver.mod' into any directory existing in 'MAYA\_MODULE\_PATH', then change the paths in it and make them point to the right position, maya will find it without difficulty. 

* There's a backup of 'DeformationLearningSolver.mod' in 'modules' folder, you can copy and paste it to anywhere rather than modify it, otherwise, 'install.mel' will fail to install.

* Launch it with these python commands:
> import DLS 	
> DLS.launch()

## Features:
* Convert deformation animation such as blend shapes, to skinned, weighted and bone joint animation. 
* Approximate deformation animation by solving the skinning weights with existing joints and joint animations.
* Reverse skeleton animations from animated sequences with existing joints and skinning weights.

## Limitations:
* Work with single mesh each time.

## Plug-ins:
These plug-ins are included in this tool

* SSDSolverCmd: the core functions of SSDR.
* wbDeltaMushDeformer: a deformer based on [Delta Mush: Smoothing Deformations While Preserving Detail](http://dl.acm.org/citation.cfm?id=2633376), it's also a component in AdvanceSkeleton since 5.0.

## Usage:
- There's no document for this tool yet, the only instruction you can find are those two Demos mentioned above.

- This tool can either solve the best weight map with pre-define joints by user or extract specify number of joints, animations and weight map from a mesh sequences, the first case is extremely fast since it only need to solve the weight map with one iteration.

- To solve weight map from existing joints, please bind mesh with skin cluster first, this tool will find joints involve, then put them into solver. Otherwise, it will solve mesh sequences with specify number of joints within max iterations.

### Parameters:
Here are key parameters you should understand:

- **Num of Bones**: specifies the number of joints will be created.
- **Max Infs**: specifies the maximum number of weighted influences for a given point.
- **Epsilon**: the computation will finish before it reaches the max iteration if the subtraction between Current Total Error and Previous Total Error is less than epsilon.
- **Max Iters**: in general, more iterations can result in more accurate approximation, but I found 10 is sufficient in most cases.
- **Target Mesh**: input animated mesh here will enable reverse enginnering feature as showed in [Demo v1.5](https://vimeo.com/138048608).

## Technical Support:
There’s no technical support for free users.

## Further Development:
Everything at this stage is uncertain, it would be the first and the last version I could share.

## Notes:
* For anyone who wants to convert delta mush to skinning, this isn't the best solution for it, since the computation is too heavy, please turn to tools like: [Semi Auto Skinning R&D
](http://robotsquids.blogspot.com/2014/09/semi-auto-skinning-r.html), [Skonverter](https://github.com/coxevan/skonverter).

* Clone or not clone? For those people think I stole the idea from Skinning Converter by Hans Godard, you're free to comment at your pleasure :)

## History:
#### 2015-11-21: v1.5.3 by Webber Huang
- UPDATE: wbDeltaMush v1.8.0, better performance and minor bugs fixed

#### 2015-09-02: [v1.5.0](http://riggingtd.com/2015/09/deformation-learning-solver-v1-5/) by Webber Huang
- NEW: wbDeltaMush is included
- NEW: reverse bone animation from animated sequence
- NEW: alternative update with existing bones and weights
- NEW: a editor for sampling any attribute
- UPDATE: parallelize bone transformation updating function, 30~40% faster than before
- minor bugs fixed

#### 2015-06-18: [v1.0.0](http://riggingtd.com/2015/06/deformation-learning-solver/) by Webber Huang
- Initial release


## References:
1. B. H. Le and Z. Deng, “Smooth Skinning Decomposition with Rigid Bones,” ACM Trans. Graph., vol. 31, no. 6, pp. 199:1–199:10, Nov. 2012.
2. Hans Godard, [Skinning Converter](https://vimeo.com/123883474)