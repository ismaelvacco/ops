from fabric.api import env, local, require
import os

def compare_versions(x, y):
    """
    Expects 2 strings in the format of 'X.Y.Z' where X, Y and Z are
    integers. It will compare the items which will organize things
    properly by their major, minor and bugfix version.
    ::

        >>> my_list = ['v1.13', 'v1.14.2', 'v1.14.1', 'v1.9', 'v1.1']
        >>> sorted(my_list, cmp=compare_versions)
        ['v1.1', 'v1.9', 'v1.13', 'v1.14.1', 'v1.14.2']

    """
    def version_to_tuple(version):
        # Trim off the leading v
        version_list = version[1:].split('.', 2)
        if len(version_list) <= 3:
            [version_list.append(0) for _ in range(3 - len(version_list))]
        try:
            return tuple((int(version) for version in version_list))
        except ValueError: # not an integer, so it goes to the bottom
            return (0, 0, 0)

    x_major, x_minor, x_bugfix = version_to_tuple(x)
    y_major, y_minor, y_bugfix = version_to_tuple(y)
    return (cmp(x_major, y_major) or cmp(x_minor, y_minor)
            or cmp(x_bugfix, y_bugfix))

def store_deployed_version():
    if env.sha_url_template:
        env.deployed_version = local('curl -s %s' % sha_url()).strip('"')

def sha_url():
    require('sha_url_template')
    if env.deployment_type == 'PRODUCTION':
        subdomain = 'www.'
    else:
        subdomain = env.deployment_type.lower() + '.'
    return env.sha_url_template % subdomain

def absolute_release_path():
    require('path')
    require('current_release_path')
    return os.path.join(env.path, env.current_release_path)