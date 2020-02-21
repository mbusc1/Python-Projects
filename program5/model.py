import controller, sys
import model   # Pass a reference to this model module to update calls in update_all Use the reference to this module to pass it to update methods

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special   import Special

# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running = False
select = ''
cycle_count = 0
objs = set()
sim = None


#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running,cycle_count,balls,objs
    running     = False
    cycle_count = 0
    objs        = set()
    display_all()

#start running the simulation
def start ():
    global running
    running = True


#stop running the simulation (freezing it)
def stop ():
    global running
    running = False


#tep just one update in the simulation
def step ():
    global cycle_count, objs
    cycle_count += 1
    for ob in objs:
        ob.update()


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global select
    select = kind


#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    global objs, select
    obj_rem = None
    if select == 'Remove':
        for ob in objs:
            if ob.contains((x,y)):
                obj_rem = ob
        model.remove(obj_rem)
    else:
        exec('global sim\nsim = '+select+str((x,y)))
        #print(sim)
        model.add(sim)
        #print(objs)


#add simulton s to the simulation
def add(s):
    global objs
    objs.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    global objs
    if s in objs:
       objs.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    global objs
    return set(ob for ob in objs if p(ob))


#call update \(pass model as its argument\) for every simulton in the simulation
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global cycle_count, objs
    if running:
        cycle_count += 1
        ret = set()
        for ob in objs:
            if ob.update() != None:
                ret = ret.union(ob.update())
        #print(ret)
        #asynchronously remove destroyed simultons to not urin update all iteration
        if ret != set():
            for r in ret:
                model.remove(r)

#delete every simulton from the canvas in the simulation; then call display on each
#  simulton being simulated to add it back to the canvas, possibly in a new location, to
#  animate it; also, update the progress label defined in the controller
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    global objs
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
    #print(objs)
    for ob in objs:
        if ob != None:
            ob.display(controller.the_canvas)
        
    controller.the_progress.config(text=str(len(objs))+" simulations/"+str(cycle_count)+" cycles")
