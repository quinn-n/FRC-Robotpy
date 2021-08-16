*round -- this was my version control. They didn't have any kind of internet access at competition, and I wanted to be able to easily switch between versions if I needed to. Each round is an iteration of code - a new feature may have been added, a risky bugfix that I wanted to have the old version of the code for just in case it didn't work, etc.

Tests - My test code for various features and functions. I got tired of rewriting logic for 4 wheels for each new feature, and instead just wrote code for 1 and it made everything much easier.

cscore.py -- (legacy code) this was what I used to be able to deploy my code to the robot, since the library doesn't exist for ubuntu. It was just enough for me to be able to run the 'deploy' feature with wpilib.

Mechanum - code for a mechanum drive terrain. Should work just fine, although I'm not sure if I changed it since I last used it.

ctreEncoders - tank drive with ctre's encoders that go with their talon SRX's. Not yet tested on a full robot yet.


wpilibCameras - legacy code. When I used to use ubuntu, I couldn't use the cscore library because they haven't come out with one for a regular linux distribution (only the one that runs on the robot has it I think), and so I needed to use the standard way that only works with one camera for the sim. The reason I kept putting up with the cscore thing was because it was more robust and allowed us to have multiple cameras. I now use arch linux as my regular distribution, so I no longer even need to worry about getting the sim feature to work!
