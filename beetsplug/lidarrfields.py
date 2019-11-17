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
    
    self.template_fields['releasegroupartist'] = self._tmpl_releasegroupartist
    self.template_fields['lidarralbum'] = self._tmpl_lidarralbum

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
