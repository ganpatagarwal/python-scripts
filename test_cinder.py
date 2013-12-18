import commands as cs
import time
import os
import sys
import timeit

cmd_for_vol_status = 'cinder list'
cmd_for_snap_status = 'cinder snapshot-list'
job_status = {}


def check_status(cmd,entity_name):
    time.sleep(10)
    output = cs.getoutput(cmd).split('\n')
    #print output
    for line in output:
        if line.find(entity_name)>=0:
            if line.find('creating')>=0:
                print "current status is : creating"
                time.sleep(20)
                return check_status(cmd,entity_name)
            elif line.find('deleting')>=0:
                print "current status is : deleting"
                time.sleep(20)
                return check_status(cmd,entity_name)
            elif line.find('available')>=0:
                vol_id = line.split('|')[1].strip()
                print "found ID : ",vol_id
                return vol_id
            elif line.find('Running')>=0:
                id = line.split('|')[1].strip()
                print "found ID : ",id
                return id
            else:
                return None

def create_volume(volume_name,volume_size):
    global cmd_for_vol_status
    op_stats={}
    timer_start = timeit.default_timer()
    print "Creating Volume........."
    cmd = 'cinder create --display-name %s %s'%(volume_name,volume_size)
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        volume_id = check_status(cmd_for_vol_status,volume_name)
        if volume_id is not None:
            print "Volume created successfully"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Success'
            op_stats['Volume Name']=volume_name
            op_stats['Volume Size(in GB)']=volume_size
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create volume']=op_stats
            return volume_id            
        else:
            print "Error in creating volume"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Error'
            op_stats['Volume Name']=volume_name
            op_stats['Volume Size(in GB)']=volume_size
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create volume']=op_stats
            return None
    else:
        print "Error in creating volume"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Volume Name']=volume_name
        op_stats['Volume Size(in GB)']=volume_size
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['create volume']=op_stats
        return None

def delete_volume(volume_id,volume_name):
    global cmd_for_vol_status
    op_stats={}
    timer_start = timeit.default_timer()
    print "Deleting Volume........."
    cmd = 'cinder delete %s'%volume_id
    print 'COMMAND : ',cmd
    rc = os.system(cmd)
    if rc == 0:
        volume_id = check_status(cmd_for_vol_status,volume_id)
        if volume_id is None:
            print "Volume deleted successfully"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Success'
            op_stats['Volume Name']=volume_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['delete volume']=op_stats
        else:
            print "Error in deleting volume"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Error'
            op_stats['Volume Name']=volume_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['delete volume']=op_stats
    else:
        print "Error in deleting volume"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Volume Name']=volume_name
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['delete volume']=op_stats

def create_snapshot(volume_id,snapshot_name):
    global cmd_for_snap_status
    op_stats={}
    timer_start = timeit.default_timer()
    print "Creating Snapshot............."
    cmd = 'cinder snapshot-create --display-name %s %s'%(snapshot_name,volume_id)
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        snapshot_id = check_status(cmd_for_snap_status,snapshot_name)
        if snapshot_id is not None:
            print "Snapshot created successfully"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Success'
            op_stats['Snapshot Name']=snapshot_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create snapshot']=op_stats
            return snapshot_id
        else:
            print "Error in creating snapshot"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Error'
            op_stats['Snapshot Name']=snapshot_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create snapshot']=op_stats
            return None
    else:
        print "Error in creating snapshot"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Snapshot Name']=snapshot_name
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['create snapshot']=op_stats
        return None

def delete_snapshot(snapshot_id,snapshot_name):
    global cmd_for_snap_status
    op_stats={}
    timer_start = timeit.default_timer()
    print 'Deleting Snapshot..................'
    cmd = 'cinder snapshot-delete %s'%snapshot_id
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        snapshot_id = check_status(cmd_for_snap_status,snapshot_id)
        if snapshot_id is None:
            print "Snapshot deleted successfully"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Success'
            op_stats['Snapshot Name']=snapshot_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['delete snapshot']=op_stats
        else:
            print "Error in deleting snapshot"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Error'
            op_stats['Snapshot Name']=snapshot_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['delete snapshot']=op_stats
    else:
        print "Error in deleting snapshot"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Snapshot Name']=snapshot_name
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['delete snapshot']=op_stats

def create_cloned_volume(clone_name,volume_id,volume_size):
    global cmd_for_vol_status
    op_stats={}
    timer_start = timeit.default_timer()
    print "Creating cloned Volume........."
    cmd = 'cinder create --source-volid %s --display-name %s %s'%(volume_id,clone_name,volume_size)
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        volume_id = check_status(cmd_for_vol_status,clone_name)
        if volume_id is not None:
            print "Volume clone created successfully"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Success'
            op_stats['Clone Name']=clone_name
            op_stats['Clone Size(in GB)']=volume_size
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create cloned volume']=op_stats
            return volume_id
        else:
            print "Error in creating volume clone"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Error'
            op_stats['Clone Name']=clone_name
            op_stats['Clone Size(in GB)']=volume_size
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create cloned volume']=op_stats
            return None
    else:
        print "Error in creating volume clone"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Clone Name']=clone_name
        op_stats['Clone Size(in GB)']=volume_size
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['create cloned volume']=op_stats
        return None

def create_volume_from_snapshot(snapshot_id,volume_name,volume_size):
    global cmd_for_vol_status
    op_stats={}
    timer_start = timeit.default_timer()
    print "Creating volume from snapshot............"
    cmd = 'cinder create --snapshot-id %s --display-name %s %s'%(snapshot_id,volume_name,volume_size)
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        volume_id = check_status(cmd_for_vol_status,volume_name)
        if volume_id is not None:
            print "Volume from snapshot created successfully"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Success'
            op_stats['Volume Name']=volume_name
            op_stats['Volume Size(in GB)']=volume_size
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create volume from snapshot']=op_stats
            return volume_id
        else:
            print "Error in creating volume from snapshot"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Error'
            op_stats['Volume Name']=volume_name
            op_stats['Volume Size(in GB)']=volume_size
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create volume from snapshot']=op_stats
            return None
    else:
        print "Error in creating volume from snapshot"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Volume Name']=volume_name
        op_stats['Volume Size(in GB)']=volume_size
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['create volume from snapshot']=op_stats
        return None

def create_instance(image_name,flavor,instance_name):
    op_stats={}
    timer_start = timeit.default_timer()
    print "Creating instance...................."
    cmd = '''nova boot --image %s --flavor="%s" %s'''%(image_name,flavor,instance_name)
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        instance_id = check_status("nova list",instance_name)
        if instance_id is not None:
            print "Instance launched successfully"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Success'
            op_stats['Instance Name']=instance_name
            op_stats['Image Name']=image_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create instance']=op_stats
            return instance_id
        else:
            print "Error in launching instance"
            timer_stop = timeit.default_timer()
            time_taken = timer_stop-timer_start
            op_stats['Status']='Error'
            op_stats['Instance Name']=instance_name
            op_stats['Image Name']=image_name
            op_stats['Time Taken(in Seconds)']=time_taken
            job_status['create instance']=op_stats
            return None
    else:
        print "Error in launching instance"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Instance Name']=instance_name
        op_stats['Image Name']=image_name
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['create instance']=op_stats
        return None

def attach_volume(instance_id,volume_id,drive_location,instance_name,volume_name):
    op_stats={}
    timer_start = timeit.default_timer()
    print "Attaching volume to instance.............."
    cmd = 'nova volume-attach %s %s %s'%(instance_id,volume_id,drive_location)
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        print "Volume Attached successfully"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Success'
        op_stats['Instance Name']=instance_name
        op_stats['Volume Name']=volume_name
        op_stats['Drive Location']=drive_location
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['attach volume']=op_stats
    else:
        print "Error in volume attach"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Instance Name']=instance_name
        op_stats['Volume Name']=volume_name
        op_stats['Drive Location']=drive_location
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['attach volume']=op_stats

def detach_volume(instance_id,volume_id,instance_name,volume_name):
    op_stats={}
    timer_start = timeit.default_timer()
    print "DetachingVolume from instance..............."
    cmd = 'nova volume-detach %s %s'%(instance_id,volume_id)
    print "COMMAND : ",cmd
    rc = os.system(cmd)
    if rc == 0:
        print "Volume detached successfully"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Success'
        op_stats['Instance Name']=instance_name
        op_stats['Volume Name']=volume_name
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['detach volume']=op_stats
    else:
        print "Error in volume detach"
        timer_stop = timeit.default_timer()
        time_taken = timer_stop-timer_start
        op_stats['Status']='Error'
        op_stats['Instance Name']=instance_name
        op_stats['Volume Name']=volume_name
        op_stats['Time Taken(in Seconds)']=time_taken
        job_status['detach volume']=op_stats


#testing starts here------------------------------------------

test_volume_name = 'vol_test_inst2'
vol_size_gb = '10'
test_snapshot_name = 'snap_test1'
test_clone_name = 'clone_test2'
test_vol_from_snap_name = 'vol_from_snap_test1'
instance_image_name = 'cirros-0.3.1-x86_64-uec'
flavor = 1
instance_name = 'cirror_inst1'
mount_point = '/dev/vdc'

#creating volume
vol_id1 = create_volume(test_volume_name,vol_size_gb)

#create snapshot
snap_id1 = create_snapshot(vol_id1,test_snapshot_name)

#create cloned volume
vol_id2 = create_cloned_volume(test_clone_name,vol_id1,vol_size_gb)

#create volume from snapshot
vol_id3 = create_volume_from_snapshot(snap_id1,test_vol_from_snap_name,vol_size_gb)

#create instance
inst_id1 = create_instance(instance_image_name,flavor,instance_name)

#attach volume
attach_volume(inst_id1,vol_id1,mount_point,instance_name,test_volume_name)

#delete volume created from snapshot
#delete_volume(vol_id3,test_vol_from_snap_name)

#delete clone volume
#delete_volume(vol_id2,test_clone_name)

#delete snapshot
#delete_snapshot(snap_id1,test_snapshot_name)

#detach volume
#detach_volume(inst_id1,vol_id1,instance_name,test_volume_name)

#deleting volume
#delete_volume(vol_id1,test_volume_name)


print '\n*************************  SUMMARY  *****************************'
keys=job_status.keys()
keys.sort()
for key in keys:
    #print key,job_status[key]
    print "\n-------------------------------------------------------\n"
    print "Operation Performed : ",key
    stats = job_status[key]
    stats_keys=stats.keys()
    stats_keys.sort()
    col_width = max(len(word) for word in stats_keys) + 2
    for k in stats_keys:
        print "\t %s : %s"%("".join(k.ljust(col_width)),str(stats[k]))
    print "\n-------------------------------------------------------\n"
    
