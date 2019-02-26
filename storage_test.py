import os
import sys
from time import time

FILE = 'rwtest' # temp file, for write & read

def write_test(file, size_bytes):
    """Write performance test

    Parameters
    ----------
    file : str
        The file name for the temporary created file
    size_bytes : int
        A number specify the size of data to write in bytes

    Returns
    -------
    float
        A float number that is the time spent to write.
    """

    f = os.open(file, os.O_CREAT | os.O_WRONLY)
    data = os.urandom(size_bytes) # create random data with size_bytes in bytes
    start_time = time() * 1000
    os.write(f, data)
    os.fsync(f) # force os write to disk
    end_time = time() * 1000
    os.close(f)
    return end_time - start_time

def read_test(file, size_bytes):
    """Read performance test

    Parameters
    ----------
    file : str
        The file name for the temporary created file
    size_bytes : int
        A number specify the size of data to read in bytes

    Returns
    -------
    float
        A float number that is the time spent to read.
    """

    f = os.open(file, os.O_RDONLY)
    start_time = time() * 1000
    data = os.read(f, size_bytes)
    end_time = time() * 1000
    os.close(f)
    return end_time - start_time

def test(file, size, unit):
    """Test storage performance and print results

    Parameters
    ----------
    file : str
        The file name for the temporary created file
    size : int
        The number of [unit] that is going to read/write
    unit : str
        The data unit. Should be one of b, kb, mb, and gb.
    """

    size_bytes = size
    if unit.lower() == 'kb':
        size_bytes *= 1024
    elif unit.lower() == 'mb':
        size_bytes *= 1024 * 1024
    elif unit.lower() == 'gb':
        size_bytes *= 1024 * 1024 * 1024

    print('----------Storage Performance Test----------')

    wt = write_test(file, size_bytes)
    avg_ws = float(size_bytes) / wt
    print("Write %d %s in %.2f ms." % (size, unit.upper(), wt))
    print("Average writing speed: %.2f Bytes / ms" % (avg_ws))

    print('---------------------------------------------------')

    rt = read_test(file, size_bytes)
    avg_rs = float(size_bytes) / rt
    print("Read %d %s in %.2f ms." % (size, unit.upper(), rt))
    print("Average reading speed: %.2f Bytes / ms" % (avg_rs))

    print('----------------End Of Test-----------------')

    os.remove(file)

if __name__ == "__main__":
    """First do a parameters check. If the parameters are valid, do read/write test

    Parameters
    ----------
    argv[0] : str
        file name
    argv[1] : int
        number of [unit(argv[2])] that is going to read/write
    argv[2] : str
        unit, case insensitive.
        Including B, KB, MB, GB.
    """

    if len(sys.argv) != 3 or sys.argv[2].lower() not in ['b', 'kb', 'mb', 'gb']: # parameters check
        print('Usage error, pls try again.')
        print('Usage: python [file_name].py [size] [unit]')
        print('Example: python storage_test.py 10 kb')
    else:
        size = int(sys.argv[1])
        unit = sys.argv[2]

        test(FILE, size, unit)