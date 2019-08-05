# T-Drive Taxi Trajectory Reconstruction



## Objective:
In this study we intend to develop methods which can learn the sequence dependence between the positional coordinates of trajectories, and then can be used to reconstruct the missing portions in these trajectories.

## Dataset:
T-Drive trajectory dataset contains a one-week trajectories of 10,357 taxis in Beijing. You can find the original dataset [here](https://drive.google.com/file/d/1pzaGZaboOdUxsw7l6hhJDdsH8ZqUeZXs/view?usp=sharing).

## Notebooks:
1. Data Preparation:[CollateData.ipynb] (https://github.com/Shivam0712/TrajectoryReconstruction/blob/master/CollateData.ipynb)
2. Data Exploration:[TDriveExplore.ipynb](https://github.com/Shivam0712/TrajectoryReconstruction/blob/master/TDriveExplore.ipynb)
3. Trip Segmentation:[TaxiTrajectorySegmentationSpeed.py](https://github.com/Shivam0712/TrajectoryReconstruction/blob/master/TaxiTrajectorySegmentationSpeed.py)
4. Trip Segmentation and Analysis:[TaxiTrajectorySegmentationAnalysis.ipynb](https://github.com/Shivam0712/TrajectoryReconstruction/blob/master/TaxiTrajectorySegmentationAnalysis.ipynb)
5. Linear Interpolation:[LinearInterpolationTime.py](https://github.com/Shivam0712/TrajectoryReconstruction/blob/master/LinearInterpolationTime.py)[LinearInterpolationDistance.py](https://github.com/Shivam0712/TrajectoryReconstruction/blob/master/LinearInterpolationDistance.py)
6. Linear Interpolation Analysis:[LinearInterpolationResults.ipynb](https://github.com/Shivam0712/TrajectoryReconstruction/blob/master/LinearInterpolationResults.ipynb)
