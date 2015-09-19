"""
@copyright: Copyright (C) 2014 EMC.  All rights reserved.

@summary:   This is the library Class to invoke XtremIO 3.0 RESTful API Version 1.0.

"""

import json
import os
import sys, traceback
import urllib, urllib2, base64

from distutils.version import StrictVersion
from base_utils import ESILogger


class XtremIORestCalls(object):
    """
    This class calls the REST APIs of XtremIO
    """
    XIOS_V3 = '3.0.0'
    XIOS_V4 = '4.0.0'
    logger=ESILogger.get_logger(__name__)
    
    def _req(self, server_data, command=None, payload=None, req_type=None):
        """Creates and sends request to XtremIO array"""
        ip = server_data.get('admin_host')
        username = server_data.get('admin_user')
        password = server_data.get('admin_passwd')
        if not (ip and username and password):
            raise RuntimeError('Incorrect value passed for authentication.')
        baseurl = "https://%s/api/json/types/" % ip
        if command and not "https" in command:
            url = baseurl + command
        elif command:
            url = command
        else:
            url = baseurl

        try:
            if not payload:
                # HTTP GET
                request = urllib2.Request(url)
            else:
                # HTTP POST
                request = urllib2.Request(url, data=json.dumps(payload))

            base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
            if req_type:
                request.get_method = lambda: req_type
            result = urllib2.urlopen(request)
        except (urllib2.HTTPError,) as exc:
            if exc.code == 400 and hasattr(exc, 'read'):
                error = json.load(exc)
                if error['message'].endswith('_not_found'): 
                    raise RuntimeError('Resource is not available.')
                elif error['message'].endswith('name_not_unique'):
                    raise RuntimeError('Resource by this name already exists.')
                elif error['message'].endswith('too_many_vol_obj'):
                    raise RuntimeError('Maximum allowed volumes limit exceeded.')
                elif error['message'].endswith('too_many_objs'):
                    raise RuntimeError('Maximum allowed snapshots per volume exceeded.')
                else:
                    raise RuntimeError(str(error['message']))
            elif exc.code == 401:
                error = json.load(exc)
                raise RuntimeError(error['message'])
        if result.code >= 300:
            msg = (('bad response from XMS got http code %(code)d, %(msg)s') % {'code': result.code, 'msg': result.msg})
            raise RuntimeError(msg)
        return result
    
    def _safe_cast_to_int(self, val, parameter_desc = "Input Parameter"):
        try:
            result = int(val)
        except (ValueError, TypeError):
            raise RuntimeError('Invalid %s.' % parameter_desc)
        if result <= 0:
            raise RuntimeError('Invalid %s.' % parameter_desc)
        return result
     

    def validate(self, server_data):
        """Validates connection with XtremIO array"""
        result = self.get_cluster_info(server_data)
        self.logger.info("Cluster Name:    %s" % str(result[1]))
        is_valid_version = bool(StrictVersion(result[2]) >= StrictVersion(XtremIORestCalls.XIOS_V3) 
                                and StrictVersion(result[2]) < StrictVersion(XtremIORestCalls.XIOS_V4))
        is_valid = bool(result[0] == 200 and is_valid_version)
        err_msg = "" if is_valid else "Invalid Plug-in Private Data : For XtremIO 3.0 enter \"XtremIO\" and for XtremIO 4.0 enter \"XtremIO_<Cluster Name>\""
        return (is_valid, err_msg)

    def add_volume(self, server_data, volume_data):
        """Adding a New Volume and return a dictionary"""
        # Volume attributes
        volume_name = volume_data.get('name')
        size = volume_data.get('size')
        if not size:
            raise RuntimeError('Volume disk space size unavailable.')
        tmp_size = int(int(size) / 1024 / 1024)
        volume_size = str(tmp_size) + 'm'
        volume_parent_folder = volume_data.get('folder', '/')

        # post data
        payload = {"vol-name":volume_name,
                 "vol-size":volume_size,
                 "parent-folder-id":volume_parent_folder
                 }
        command = 'volumes/'

        try:
            resp = self._req(server_data, command, payload)
        except Exception, error:
            raise RuntimeError('Could Not Add Volume : %s. ' % volume_name + str(error.message))
        data = json.loads(resp.read())
        vol_content = self.get_resource_details_by_url(server_data, data.get('links')[0])
        return vol_content

    def delete_volume(self, server_data, volume_data):
        """Deleting a Volume"""
        # Volume attributes
        volume_name = volume_data.get('name')
        if not volume_name:
            raise RuntimeError('Volume name missing.')
        command = 'volumes/?name=%s' % urllib.quote_plus(volume_name)
        try:
            self._req(server_data, command, req_type='DELETE')
        except Exception, error:
            raise RuntimeError('Could Not Delete Volume : %s. ' % volume_name + str(error.message))

    def extend_volume(self, server_data, volume_data, new_volume_size): 
        """Extending Volume size"""
        # Volume attributes
        volume_name = volume_data.get('name')
        tmp_size = int(new_volume_size / 1024 / 1024)
        volume_size = str(tmp_size) + 'm'

        # post data
        payload = { "vol-size":volume_size}

        command = 'volumes/?name=%s' % urllib.quote_plus(volume_name)
        try:
            resp = self._req(server_data, command, payload, 'PUT')
        except Exception, error:
            raise RuntimeError('Could Not Modify Volume : %s. ' % volume_name + str(error.message))

        # the volume data dictionary with new volume data
        volume_data['size'] = new_volume_size
        return volume_data

    def get_volume_details_by_name(self, server_data, volume_data):
        """Get Details of a Volume using Volume's name and returns a dictionary"""
        # Volume attributes
        volume_name = volume_data.get('name')
        if not volume_name:
            raise RuntimeError('Volume name missing.')

        command = 'volumes/?name=%s' % urllib.quote_plus(volume_name)
        try:
            resp = self._req(server_data, command)
        except Exception, error:
            raise RuntimeError('Failed to get %s details. ' % volume_name + str(error.message))
        data = json.loads(resp.read())
        return data.get('content')
    
    def get_volume_details_by_id(self, server_data, volume_data):
        """Get Details of a Volume using Volume's id and returns a dictionary"""
        # Volume attributes
        volume_id = self._safe_cast_to_int(volume_data.get('id'), 'Volume id')

        command = 'volumes/%s' % volume_id
        try:
            resp = self._req(server_data, command)
        except Exception, error:
            raise RuntimeError('Failed to get VolumeID[%s] details. ' % volume_id + str(error.message))
        data = json.loads(resp.read())
        return data.get('content')

    def get_resource_details_by_url(self, server_data, url):
        """Get Details of a Volume/Initiator using their url and return a dictionary"""
        try:
            resource_url = url.get('href')
            resource_resp = self._req(server_data, resource_url)
            resource_data = json.loads(resource_resp.read())
            resource_content = resource_data.get('content')
        except Exception, error:
            raise RuntimeError(str(error.message))
        return resource_content

    def list_volumes(self, server_data):
        """Get the Volumes List and return a List"""
        try:
            resp = self._req(server_data, 'volumes')
            data = json.loads(resp.read())
            vols = data.get('volumes')
            volumes = []
            for vol in vols:
                vol_content = self.get_resource_details_by_url(server_data, vol)
                volumes.append(vol_content)
        except Exception, error:
            raise RuntimeError('Failed to list volumes. ' + str(error.message))
        return volumes

    def get_storage_array(self, server_data):
        """Get the Details of the Managed Cluster and return a dictionary"""
        cluster_name = self.get_cluster_info(server_data)[1]
        command = 'clusters/?name=%s' % urllib.quote_plus(cluster_name)
        try:
            resp = self._req(server_data, command)
        except Exception, error:
            raise RuntimeError('Failed to get storage details. ' + str(error.message))
        data = json.loads(resp.read())
        return data.get('content')

    def get_cluster_info(self, server_data):
        """Get Managed Cluster's info, 
        returns (response code, Cluster name, xtremio s/w version)"""
        command = 'clusters'
        try:
            resp = self._req(server_data, command)
        except Exception, error:
            raise RuntimeError('Failed to get Cluster details. ' + str(error.message))
        data = json.loads(resp.read())
        cluster = data.get('clusters')[0]
        cluster_content = self.get_resource_details_by_url(server_data, cluster)
        sw_version = str(cluster_content.get('sys-sw-version')).split('-')
        return (resp.code, cluster.get('name'), sw_version[0])

    def create_snapshot(self, server_data, volume_data, snapshot_data = None):
        """Creating a Snapshot of a Volume and return a dictionary"""
        # snapshot attributes
        volume_name = volume_data['name']
        snaphot_name = snapshot_data.get('name', None)
        snapshot_folder = snapshot_data.get('folder', '/')
            
        if not volume_name:
            raise RuntimeError('Replication failed. Source volume name unavailable.')

        # post data
        payload = {"ancestor-vol-id":volume_name,
                 "snap-vol-name":snaphot_name,
                  "folder-id":snapshot_folder
                 }
        command = 'snapshots/'
        try:
            resp = self._req(server_data, command, payload)
        except Exception, error:
            raise RuntimeError('Replication for source [%s] failed. ' % volume_name + str(error.message))

        # retrieving the snapshot details
        data = json.loads(resp.read())
        snap_content = self.get_resource_details_by_url(server_data, data['links'][0])
        return snap_content

    def delete_snapshot(self, server_data, snapshot_data):
        """Deleting a Volume's Snapshot"""
        # snapshot attributes
        snaphot_name = snapshot_data.get('name')
        command = 'volumes/?name=%s' % urllib.quote_plus(snaphot_name)
        try:
            self._req(server_data, command, req_type='DELETE')
        except Exception, error:
            raise RuntimeError('could not delete snapshot %s. ' % snaphot_name + str(error.message))

    def get_snapshot_details_by_name(self, server_data, snapshot_data):
        """Get the Details of a Snapshot using Snapshot name and return a dictionary"""
        # snapshot attributes
        snaphot_name = snapshot_data.get('name')

        command = 'snapshots/?name=%s' % urllib.quote_plus(snaphot_name)
        try:
            resp = self._req(server_data, command)
        except Exception, error:
            raise RuntimeError('failed to get snapshot %s details. ' % snaphot_name + str(error.message))
        data = json.loads(resp.read())
        return data.get('content')

    def list_snapshots(self, server_data):
        """Get the List of Snapshots"""
        command = 'snapshots'
        try:
            resp = self._req(server_data, command)
            snaps = json.loads(resp.read()).get('snapshots')
            snapshots = []
            for snap in snaps:
                snap_content = self.get_resource_details_by_url(server_data, snap)
                snapshots.append(snap_content)
        except Exception, error:
            raise RuntimeError('failed to list snapshots. ' + str(error.message))
        return snapshots

    def add_initiator_group(self, server_data, initiator_group_data):
        """Adding an Initiator Group and return Initiator Group ID"""
        # Initiator group data
        initiator_group_name = initiator_group_data.get('grp_name')
        parent_folder = initiator_group_data.get('folder', '/')
        
        if not initiator_group_name:
            raise RuntimeError('Add initiator-groups failed. Initiator group name missing.')

        # post data
        payload = {"ig-name":initiator_group_name,
                 "parent-folder-id":parent_folder}

        command = 'initiator-groups'

        try:
            resp = self._req(server_data, command, payload)
        except Exception, error:
            raise RuntimeError('Add initiator-groups %s failed. ' % initiator_group_name + str(error.message))
        data = json.loads(resp.read())
        return int(str(data.get('links')[0].get('href')).split('/')[-1])
    
    def list_initiator_groups(self, server_data):
        """Get the List of Initiator Groups-content dictionaries"""
        command = 'initiator-groups'
        try:
            resp = self._req(server_data, command)
            data = json.loads(resp.read())
            igs = data.get('initiator-groups')
            ig_list = []
            for ig in igs:
                ig_content = self.get_resource_details_by_url(server_data, ig)
                ig_list.append(ig_content)
        except Exception, error:
            raise RuntimeError('List initiator-groups failed. ' + str(error.message))
        return ig_list
    
    def list_initiators(self, server_data):
        """Get the List of Initiator-content dictionaries"""
        command = 'initiators'
        try:
            resp = self._req(server_data, command)
            data = json.loads(resp.read())
            initiators = data.get('initiators')
            initiators_list = []
            for initiator in initiators:
                initiator_content = self.get_resource_details_by_url(server_data, initiator)
                initiators_list.append(initiator_content)
        except Exception, error:
            raise RuntimeError('List initiators failed. ' + str(error.message))
        return initiators_list
    
    def get_initiator_details_by_name(self, server_data, initiator_data):
        """Get Details of a Initiator using Initiator's name"""
        initiator_name = initiator_data.get('name')
        command = 'initiators/?name=%s' % urllib.quote_plus(initiator_name)
        try:
            resp = self._req(server_data, command)
        except Exception, error:
            raise RuntimeError('Failed to get %s details. ' % initiator_name + str(error.message))
        data = json.loads(resp.read())
        return data.get('content')
    
    def add_initiator(self, server_data, initiator_data):
        """Adding an Initiator"""
        # Initiator data
        ig_id = self._safe_cast_to_int(initiator_data.get('ig_id'), 'Initiator Group ID')
        port_address = initiator_data.get('port_address')
        
        self.logger.debug("ig_id[%s]" % ig_id)
        self.logger.debug("port_address[%s]" % port_address)
        
        if not (port_address):
            raise RuntimeError('Add initiator failed. Insufficient value supplied.')

        # post data
        payload = {"ig-id":ig_id,
                 "port-address":port_address}

        command = 'initiators'

        try:
            resp = self._req(server_data, command, payload)
        except Exception, error:
            raise RuntimeError('Add initiator failed. ' + str(error.message))
        data = json.loads(resp.read())
        initiator_content = self.get_resource_details_by_url(server_data, data.get('links')[0])
        return initiator_content
    
    def get_initiator_group_details_by_name(self, server_data, initiator_group_data):
        """Get Details of a Initiator Group using Initiator's name"""
        ig_name = initiator_group_data.get('grp_name')
        command = 'initiator-groups/?name=%s' % urllib.quote_plus(ig_name) 
        try:
            resp = self._req(server_data, command)
        except Exception, error:
            raise RuntimeError('Failed to get %s details. ' % ig_name + str(error.message))
        data = json.loads(resp.read())
        return data.get('content')
    
    def create_lun_mapping(self, server_data, volume_data, initiator_group_data):
        """Creating a LUN Mapping and returns lun-mapping ID"""
        # Initiator data
        ig_id = self._safe_cast_to_int(initiator_group_data.get('index'), 'Initiator Group id')
        # Volume attributes
        volume_id = self._safe_cast_to_int(volume_data.get('id'), 'Volume id')
        
        self.logger.debug("ig_id[%s]" % ig_id)
        self.logger.debug("volume_id[%s]" % volume_id)
        
        # post data
        payload = {"vol-id":volume_id,
                 "ig-id":ig_id}

        command = 'lun-maps'

        try:
            print payload
            resp = self._req(server_data, command, payload)
        except Exception, error:
            raise RuntimeError('LUN Mapping creation failed. ' + str(error.message))
        data = json.loads(resp.read())
        return int(str(data.get('links')[0].get('href')).split('/')[-1])
    
    def remove_initiator_group(self, server_data, initiator_group_data):
        """Removing an Initiator Group"""
        # Initiator group data
        ig_id = self._safe_cast_to_int(initiator_group_data.get('index'), 'Initiator Group id')
        command = 'initiator-groups/%s' % ig_id
        try:
            self._req(server_data, command, req_type='DELETE')
        except Exception, error:
            raise RuntimeError('Could Not Delete Initiator Group[%s]. ' % ig_id + str(error.message))
        
        
    def get_lun_mapping_id(self, server_data, volume_data, initiator_group_data):
        """Get a LUN Mapping ID"""
        # Initiator Group data
        ig_id = self._safe_cast_to_int(initiator_group_data.get('index'), 'Initiator Group id')
        # Volume attributes
        volume_id = self._safe_cast_to_int(volume_data.get('id'), 'Volume id')
        
        self.logger.debug("ig_id[%s]" % ig_id)
        self.logger.debug("volume_id[%s]" % volume_id)
        
        command = 'lun-maps'
        
        try:
            resp = self._req(server_data, command)
            data = json.loads(resp.read())
            lun_maps = data.get('lun-maps')
            for lun_map in lun_maps:
                lun_map_content = self.get_resource_details_by_url(server_data, lun_map)
                if lun_map_content.get('ig-index') == ig_id and lun_map_content.get('vol-index') == volume_id:
                    return lun_map_content.get('mapping-index')
        except Exception, error:
            raise RuntimeError('Get a LUN Mapping ID failed. ' + str(error.message))
        return None
    
    def remove_lun_mapping(self, server_data, lun_mapping_data):
        """Removing a LUN Mapping"""
        command = 'lun-maps/%s' % self._safe_cast_to_int(lun_mapping_data.get('lun_maps_id'), 'LUN Mapping id')
        try:
            self._req(server_data, command, req_type='DELETE')
        except Exception, error:
            raise RuntimeError('could not delete LUN Mapping. ' + str(error.message))
        
    def remove_initiator(self, server_data, initiator_data):
        """Removing an Initiator"""
        command = 'initiators/%s' % self._safe_cast_to_int(initiator_data.get('initiator_id'), 'Initiator id')
        try:
            self._req(server_data, command, req_type='DELETE')
        except Exception, error:
            raise RuntimeError('could not delete Initiator. ' + str(error.message))
    
    def rename_initiator_group(self, server_data, initiator_group_data, new_initiator_group_name):
        """Renaming an Initiator Group"""
        # Initiator data
        ig_id = self._safe_cast_to_int(initiator_group_data.get('index'), 'Initiator Group id')

        # post data
        payload = { "initiator-group-name":new_initiator_group_name}

        command = 'initiator-groups/%s' % ig_id
        try:
            self._req(server_data, command, payload, 'PUT')
        except Exception, error:
            raise RuntimeError('Could Not Renaming Initiator Group.' + str(error.message))


#     TODO: folder and initiator related functions
    def modify_initiator(self, server_data, initiator_data, new_initiator_data):pass
    def list_lun_mappings(self, server_data):pass
    def get_lun_mapping_details_by_name(self, server_data, lun_mapping_data):pass
    def create_volume_folder(self, server_data, volume_folder_data):pass
    def rename_volume_folder(self, server_data, volume_folder_data, new_folder_name):pass
    def delete_volume_folder(self, server_data, volume_folder_data):pass
    def get_volume_folder_details_by_name(self, server_data, volume_folder_data):pass
    def list_volume_folders(self, server_data):pass
    def add_ig_folder(self, server_data, ig_folder_data):pass
    def rename_ig_folder(self, server_data, ig_folder_data, new_folder_name):pass
    def remove_ig_folder(self, server_data, ig_folder_data):pass
    def get_ig_folder_details_by_name(self, server_data, ig_folder_data):pass
    def list_ig_folders(self, server_data):pass

