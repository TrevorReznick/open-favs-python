import pkg_resources

def main(args):
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    return {"body": installed_packages}