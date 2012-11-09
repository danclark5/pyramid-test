import fcntl
#-----------------------------------------------------------------------------
# Utilities
#-----------------------------------------------------------------------------

def obtain_locked_file(fd):
    '''Create a file lock to prevent other process (that use this process of
    course) from using the resource in question.
    PARAMS
    - fd: the file descriptor of the file that is to be locked'''
    #Unix has a advisory file locking system that is controled using fcntl
    # 1 - Need to open file with builtin open (use with to close gracefully
    # 2 - attempt lock via fcntl
    #   2a - if lock successful when return file object to work on.
    #   2b - if not then close file and return an error.
    #try:
    #    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    pass

def remove_file_lock(file):
    '''Remove the lock that exists'''
    
