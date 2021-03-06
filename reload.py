from os import listdir
import os
from os.path import isfile, join

## HYPERPARAMETERS
FORMAT = '.h5'
MAX_STEPS = None

## Change working directory
os.chdir('results')

## List files
mypath = os.getcwd() ## Current path
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

## Find valid files
fs = []
for f in files:
    if FORMAT in f: 
        fs.append(f)
## If no valid files
print('')
if len(fs) == 0:
    print('No .npy files found.')
    quit()

## Show valid files
print('Select file to load:')
print('')
for i, f in enumerate(fs):
    print('  [',i, '] ', f)

## Make choice
print('')
sel = None 
while sel not in range(len(fs)):
    sel = int(input('Selection > '))

sname = fs[sel] ## Selected filename
print(sname, ' selected.')

## List of available environments
envs = ['CartPole-v0',
        'LunarLander-v2', 
        'LunarLanderContinuous-v2',
        'BipedalWalker-v2', 
        'BipedalWalkerHardcore-v2']

print('\n'+'Select environment:')
## Show envs
for i, envname in enumerate(envs):
    print('['+str(i)+'] '+envname)

## Select environment
print('')
sel = None 
while sel not in range(len(envs)):
    sel = int(input('Selection > '))

action_modes = ['argmax', 'raw']
for i, action in enumerate(action_modes):
    print('['+str(i)+'] '+action)

print('')
act_sel = None 
while act_sel not in range(len(envs)):
    act_sel = int(input('Selection > '))

action_mode = action_modes[act_sel]

from UMDAc.UMDAc import UMDAc
from UMDAc.Wrappers.Gym import Gym

### INITIALIZATION ###

## Init env
problem = Gym(envs[sel],
              iterations=1,
              max_steps=MAX_STEPS,
              action_mode=action_mode)

## Init UMDAc
umdac = UMDAc(model=None,
             problem=problem,
             gen_size=None)

umdac.load_model(sname)

from tqdm import tqdm

log = []

print('')
if input('Render environment? [Y/n]') == 'n':
    RENDER = False
else:
    RENDER = True

for i in tqdm(range(100)):
    ## Evaluate specimen, render enabled
    tr = problem.evaluate(specimen=None,
                         model=umdac.model,
                         render=RENDER,
                         verbose=RENDER)
    log.append(tr)

print('')
print('Average total reward of 100 runs: ', sum(log) / len(log))

