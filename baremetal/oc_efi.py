import os
import sys
import pathlib

from scripts import utils

efi_root = str(pathlib.PurePath(os.getcwd(), (sys.argv[1] if len(sys.argv) > 1 else '')))
is_debug = os.environ.get('EFI_DEBUG', '') != ''


#
# 1. Download and arrange required files
#

#
# 1-1. OpenCore and AMD Tweak
# https://dortania.github.io/OpenCore-Install-Guide/installer-guide/opencore-efi.html
#

print('opencore...')
opencore_url = 'https://github.com/acidanthera/OpenCorePkg/releases/download/0.7.2/OpenCore-0.7.2-{}.zip'
utils.FromZip(
    opencore_url.format('DEBUG'),
    opencore_url.format('RELEASE'),
    namedestpairs=[('X64/EFI/', efi_root), ('Docs/Sample.plist', f'{efi_root}/EFI/OC/')]
).drop(is_debug)

for e in pathlib.Path(efi_root, 'EFI/OC/Drivers/').iterdir():
    if e.name == 'OpenRuntime.efi':
        continue
    e.unlink()

for e in pathlib.Path(efi_root, 'EFI/OC/Tools/').iterdir():
    if e.name == 'OpenShell.efi':
        continue
    e.unlink()

print('AMD_Vanilla...')
amdvanilla_url = 'https://raw.githubusercontent.com/AMD-OSX/AMD_Vanilla/8ecef639781524ea18769ad33b556853c6643dd4/patches.plist'
utils.FromFile(
    amdvanilla_url,
    amdvanilla_url,
    str(pathlib.PurePath(efi_root, 'EFI/OC/')),
).drop(is_debug)


#
# 1-2. Non-kexts
# https://dortania.github.io/OpenCore-Install-Guide/ktext.html
#

print('HfsPlus.efi')
hfsplus_url = 'https://github.com/acidanthera/OcBinaryData/blob/95b7d4ccb9fea6af48641fc1f5bd4b57f747b235/Drivers/HfsPlus.efi'
utils.FromFile(
    hfsplus_url,
    hfsplus_url,
    str(pathlib.PurePath(efi_root, 'EFI/OC/Drivers/')),
).drop(is_debug)

print('SSDT-EC-USBX-DESKTOP.aml')
ssdt_url = 'https://github.com/dortania/Getting-Started-With-ACPI/raw/master/extra-files/compiled/SSDT-EC-USBX-DESKTOP.aml'
utils.FromFile(
    hfsplus_url,
    hfsplus_url,
    str(pathlib.PurePath(efi_root, 'EFI/OC/ACPI/')),
).drop(is_debug)


#
# 1-3. Kexts
#

kexts_dest = str(pathlib.PurePath(efi_root, 'EFI/OC/Kexts/'))
kextinfos = [
    ('https://github.com/acidanthera/VirtualSMC/releases/download/1.2.6/VirtualSMC-1.2.6-{}.zip',
     'Kexts/VirtualSMC.kext/'),
    ('https://github.com/acidanthera/Lilu/releases/download/1.5.5/Lilu-1.5.5-{}.zip', 'Lilu.kext/'),
    ('https://github.com/acidanthera/WhateverGreen/releases/download/1.5.2/WhateverGreen-1.5.2-{}.zip',
     'WhateverGreen.kext/'),
    ('https://github.com/acidanthera/AppleALC/releases/download/1.6.3/AppleALC-1.6.3-{}.zip', 'AppleALC.kext/'),
    ('https://github.com/acidanthera/NVMeFix/releases/download/1.0.9/NVMeFix-1.0.9-{}.zip', 'NVMeFix.kext/'),
    ('https://github.com/USBToolBox/kext/releases/download/1.1.0/USBToolBox-1.0.1-{}.zip', 'USBToolBox.kext/'),
]

for kinfo in kextinfos:
    urlfmt, zip_root = kinfo
    print(zip_root, '...', sep='')
    utils.FromZip(
        urlfmt.format('DEBUG'),
        urlfmt.format('RELEASE'),
        zip_root,
        kexts_dest,
    ).drop(is_debug)


print('SmallTreeIntel82576.kext...')
smalltree_url = 'https://github.com/khronokernel/SmallTree-I211-AT-patch/releases/download/1.3.0/SmallTreeIntel82576.kext.zip'
utils.FromZip(
    smalltree_url,
    smalltree_url,
    'SmallTreeIntel82576.kext/',
    kexts_dest,
).drop(is_debug)

print('AppleMCEReporterDisabler.kext...')
amcerd_url = 'https://github.com/acidanthera/bugtracker/files/3703498/AppleMCEReporterDisabler.kext.zip'
utils.FromZip(
    amcerd_url,
    amcerd_url,
    'AppleMCEReporterDisabler.kext/',
    kexts_dest
).drop(is_debug)

print('AMDRyzenCPUPowerManagement.kext...')
amdpowermgmt_url = 'https://github.com/trulyspinach/SMCAMDProcessor/releases/download/0.7/AMDRyzenCPUPowerManagement.kext.zip'
utils.FromZip(
    amdpowermgmt_url,
    amdpowermgmt_url,
    'AMDRyzenCPUPowerManagement.kext/',
    kexts_dest
).drop(is_debug)

print('SMCAMDProcessor.kext...')
smcamd_url = 'https://github.com/trulyspinach/SMCAMDProcessor/releases/download/0.7/SMCAMDProcessor.kext.zip'
utils.FromZip(
    smcamd_url,
    smcamd_url,
    'SMCAMDProcessor.kext/',
    kexts_dest
).drop(is_debug)


print('TODO: manually generate UTBMap.kext')
print('TODO: complete config.plist')
