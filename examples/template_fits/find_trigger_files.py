import glob
import numpy

week1_start=1262390400
week1_end=1262995200

week2_start=1262995020
week2_end=1263600000

week1 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_no_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week1_start and float(l.split('/')[-1][10:27]) < week1_end
]

week2 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_no_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week2_start and float(l.split('/')[-1][10:27]) < week2_end
]

numpy.savetxt('week_1_old_no.txt', week1, delimiter=',', fmt='%s')
numpy.savetxt('week_2_old_no.txt', week2, delimiter=',', fmt='%s')

week1 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_with_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week1_start and float(l.split('/')[-1][10:27]) < week1_end
]

week2 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_old_with_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week2_start and float(l.split('/')[-1][10:27]) < week2_end
]

numpy.savetxt('week_1_old_with.txt', week1, delimiter=',', fmt='%s')
numpy.savetxt('week_2_old_with.txt', week2, delimiter=',', fmt='%s')

week1 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_new_no_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week1_start and float(l.split('/')[-1][10:27]) < week1_end
]

week2 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_new_no_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week2_start and float(l.split('/')[-1][10:27]) < week2_end
]

numpy.savetxt('week_1_new_no.txt', week1, delimiter=',', fmt='%s')
numpy.savetxt('week_2_new_no.txt', week2, delimiter=',', fmt='%s')

week1 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_new_with_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week1_start and float(l.split('/')[-1][10:27]) < week1_end
]

week2 = [
    l for l in glob.glob('/home/arthur.tolley/PyCBC_changes/temp_fit_infra/pycbc/examples/injection_rerun/1_2_new_with_injs/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > week2_start and float(l.split('/')[-1][10:27]) < week2_end
]

numpy.savetxt('week_1_new_with.txt', week1, delimiter=',', fmt='%s')
numpy.savetxt('week_2_new_with.txt', week2, delimiter=',', fmt='%s')






