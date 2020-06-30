from beets.plugins import BeetsPlugin
import musicbrainzngs
import re

class LidarrFieldsPlugin(BeetsPlugin):
  def __init__(self):
    super(LidarrFieldsPlugin, self).__init__()
    
    self.mb_releasegroupid = None
    self.releasegroupartist = None
    self.mb_albumid = None
    self.lidarralbum = None
    self.mb_releasegroupid2 = None
    self.audiodisctotal = None
    
    self.template_fields['releasegroupartist'] = self._tmpl_releasegroupartist
    self.template_fields['lidarralbum'] = self._tmpl_lidarralbum
    self.template_fields['audiodisctotal'] = self._tmpl_audiodisctotal

  def _tmpl_releasegroupartist(self, item):
    if item.singleton:
      return None
    
    if item.mb_releasegroupid != self.mb_releasegroupid:
      rel = musicbrainzngs.get_release_group_by_id(item.mb_releasegroupid, ['artist-credits'])
      self.releasegroupartist = rel['release-group']['artist-credit'][0]['artist']['name']
      self.mb_releasegroupid = item.mb_releasegroupid
    
    return self.releasegroupartist
  
  def _tmpl_lidarralbum(self, item):
    if item.mb_albumid != self.mb_albumid or item.singleton:
      sp_rep = {'\\.$': ''}
      sp_rep_clean = {'.': ''}
      sp_regexp = re.compile('|'.join(sp_rep.keys()))
      temp_lidarralbum = sp_regexp.sub(lambda match: sp_rep_clean[match.group(0)], item.album)
      
      rep = {'/': '+', ':': '-', '?': '!'}
      regexp = re.compile('|'.join(map(re.escape, rep)))
      self.lidarralbum = regexp.sub(lambda match: rep[match.group(0)], temp_lidarralbum)
      
      self.mb_albumid = item.mb_albumid
    
    return self.lidarralbum

  def _tmpl_audiodisctotal(self, item):
    if item.singleton:
      return None
    
    if item.mb_releasegroupid != self.mb_releasegroupid2:
      total = 0
      
      if item.disctotal == 1:
        total = 1
      else:
        counted = []
        
        for albumitem in item.get_album().items():
          if albumitem.disc in counted:
            continue
            
          if albumitem.media not in ['Data CD', 'DVD', 'DVD-Video', 'Blu-ray', 'HD-DVD', 'VCD', 'SVCD', 'UMD', 'VHS']:
            total += 1
          
          counted.append(albumitem.disc)
          if len(counted) == item.disctotal:
            break
      
      if total == 1:
        return None
      self.audiodisctotal = str(total).zfill(2)
      self.mb_releasegroupid2 = item.mb_releasegroupid
    
    return self.audiodisctotal
