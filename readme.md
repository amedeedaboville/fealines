#Fealines
---------

The name comes from Frontal EEG Asymmetry (fea). One of the uses of this app is to plot the FEA.

#Install
---------
Download dist/main.zip, unarchive it and you should have an App you can run on OSX.

#Developing
Only tested on OSX so far. Should work fine on linux with minimal changes. Possible to use on windows.
## Dependencies
```
brew install sip
brew install pyqt
```
You also need pyliblo:
```
pip install pyliblo
```
##Installing
```
git clone git@github.com:amedeedaboville/fealines.git
cd fealines
python setup.py install

```

###Protocols
--------
A protocol is a series of steps for (eg) an experiment.
So, for example, you want to record a 2 minute calibration segment, 
then a 10 minute meditation. Or a 15 minute biofeedback session showing beta activity.

Protocols are stored in json files.

###Muse-io and data files
Fealines has to run muse-io to forward it the data on osc. 
I am thinking that we should have muse-io save the raw EEG data.
Then fealines can save json data files of protocols, such as (excuse the pseudojson)
{
protocol: {
              'date' : '12jan2015',
              steps :{
calibration: {'duration': '10 minutes' ...}
biofeedback: {'sham' : 'false' ...}
              }
          }
}
These would include the eeg data and the session metadata, and we could use their timestamps
to investigate phenomena in the raw data later.

####Recording
fealines only listens to a small fraction of osc messages. Most likely the alpha1 and alpha2, and maybe
some device info...
So far I am going to have each Step Element (graphs, inputs like checkboxes, text) save their own data.
