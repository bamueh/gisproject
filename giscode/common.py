from os.path import dirname, join

import giscode

TOPDIR = dirname(dirname(giscode.__file__))

PROCLSDIR = join(TOPDIR, 'data', 'landsat', 'resolution')
BEVDIR = join('data', 'bevoelkerungsstatistik',
              'Raumliche_Bevolkerungsstatistik_-OGD')

GOODSCENES = (
    join(PROCLSDIR,
         'LC08_L2SP_194027_20220623_20220705_02_T1_ST_B10-resolution.TIF'),
    join(PROCLSDIR,
         'LC08_L2SP_195027_20220716_20220726_02_T1_ST_B10-resolution.TIF'),
    join(PROCLSDIR,
         'LC09_L2SP_194027_20220717_20230407_02_T1_ST_B10-resolution.TIF'),
    join(PROCLSDIR,
         'LC08_L2SP_194027_20220725_20220802_02_T1_ST_B10-resolution.TIF'),
    join(PROCLSDIR,
         'LC08_L2SP_195027_20220801_20220806_02_T1_ST_B10-resolution.TIF'),
    join(PROCLSDIR,
         'LC09_L2SP_194027_20220802_20230404_02_T1_ST_B10-resolution.TIF'),
    join(PROCLSDIR,
         'LC09_L2SP_195027_20220809_20230403_02_T1_ST_B10-resolution.TIF'),
    join(PROCLSDIR,
         'LC08_L2SP_194027_20220810_20220818_02_T1_ST_B10-resolution.TIF'),

)

