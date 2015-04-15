# coding: utf-8

import requests
import sys
import json
from pprint import pprint
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
headers = {'Accept':'application/vnd.github.moondragon+json'}
LIST_REPOSITORIES_API = 'https://api.github.com/user/repos?type=owner&per_page=100&sort=created'
LIST_COLLABORATORS_API = 'https://api.github.com/repos/%s/collaborators'

if __name__ == '__main__':

  # param
  argv = sys.argv
  argc = len(argv)
  if (argc != 2):
    print 'Usage: # python %s token' % argv[0]
    quit()
  headers['Authorization'] = 'token %s' % argv[1]

  # get repositories
  res = requests.get(LIST_REPOSITORIES_API, headers=headers)
  repos = json.loads(res.text)

  # get collaborators
  repos2collaborators = []
  collaborators2repos = {}
  for i, repo in enumerate(repos):
    repo_fullname    = repo['full_name']
    repo_name        = repo['name']
    repo_description = repo['description']
    res = requests.get(LIST_COLLABORATORS_API % repo_fullname, headers=headers)
    collaborators = json.loads(res.text)
    for collaborator in collaborators:
      collaborator_name = collaborator['login']
      collaborators2repos.setdefault(collaborator_name, [])
      collaborators2repos[collaborator_name].append(repo_name + '\t' + repo_description + '\n')
      repos2collaborators.append(str(i) + '\t' + repo_name + '\t' + repo_description + '\t' + collaborator_name + '\n')

  # write files
  with open('repos2collaborators.tsv', 'w') as f:
    f = codecs.getwriter("utf-8")(f)
    f.writelines(repos2collaborators)

  with open('collaborators2repos.tsv', 'w') as f:
    f = codecs.getwriter("utf-8")(f)
    for collaborator_name, repo_names in collaborators2repos.items():
      for repo_name in repo_names:
        f.write(collaborator_name + '\t' + repo_name)
