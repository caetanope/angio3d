from heart import Heart
from config import *
import matplotlib.pyplot as plt
from multiprocessing import Process, Pipe
from vein import *

veinConfigs = []

def appendVeinConfigs(veinConfig):
    if veinConfig.disabled == True:
        return
    veinConfigs.append(veinConfig)
    if veinConfig.hasBranch:
        for veinChildConfig in veinConfig.children:
            appendVeinConfigs(veinChildConfig)

def generateVein(veinConfig, heart, child_conn):
    if veinConfig.shape == 'straight':
        vein = VeinSegment(veinConfig.begin, veinConfig.end, veinConfig.radius, heart)
    elif veinConfig.shape == 'secondDegree':
        vein = SecondDegreeVeinSegment(veinConfig.begin, veinConfig.end, veinConfig.radius, heart)
    else:
        return
    vein.calculatePoints(veinConfig.resolution)
    vein.buildVeinSections()
    if veinConfig.hasParent:
        vein.adjustThicknessToParent(veinConfig.parent.radius)
    if veinConfig.hasThinning:
        vein.applyThinning(veinConfig.thinning)
    child_conn.send(vein)
    child_conn.close()
       
if __name__ == '__main__':
    fig = plt.figure()
    subplot = fig.add_subplot(111, projection='3d')
    #img = plt.imread("examples/teste.jpg")
    #subplot.imshow(img extent=[-5, 80, -5, 30])
    
    heartConfig = HeartConfig()

    heart = Heart(heartConfig.getSize())
    for veinConfig in heartConfig.getVeinConfigs():
        appendVeinConfigs(veinConfig)

    jobs = []
    for veinConfig in veinConfigs:
        parent_conn, child_conn = Pipe()
        job = Process(target=generateVein, args=(veinConfig,heart,child_conn))
        job.start()
        jobs.append((job,parent_conn))

    for job,parent_conn in jobs:
        vein = parent_conn.recv()
        heart.veins.append(vein)
        job.join()

    heart.plotHeart(subplot)    
    heart.plotVeins(subplot)

    subplot.set_xlim3d([-1,1])
    subplot.set_ylim3d([-1,1]) 
    subplot.set_zlim3d([-1,1])

    subplot.set_xlabel('X')
    subplot.set_ylabel('Y')
    subplot.set_zlabel('Z')

    subplot.set_frame_on(False)
    subplot.set_axis_off()  

    subplot.set_box_aspect((1,1,1))

    plt.show()

    '''
    counter = 0
    while(1):
        counter += 1

        heart.setPulse(np.sin(counter/20)*0.1 + 0.9)
        heart.plotHeart(subplot)    
        heart.plotVeins(subplot)

        subplot.set_xlim3d([-1,1])
        subplot.set_ylim3d([-1,1]) 
        subplot.set_zlim3d([-1,1])

        subplot.set_xlabel('X')
        subplot.set_ylabel('Y')
        subplot.set_zlabel('Z')

        subplot.set_box_aspect((1,1,1))

        plt.draw()
        if plt.waitforbuttonpress(0.001):
            break
        
        subplot.clear()

        if counter >= 1000:
            break
    '''