import google_connect

canvasStudentImport = google_connect.importSheet("1801Student")
canvasStudentImport.drop_duplicates(inplace = True)
canvasStudentIndexed = canvasStudentImport.set_index(['login_id'])

canvasStaffImport = google_connect.importSheet("1801Staff")
canvasStaffImport.drop_duplicates(inplace = True)
canvasStaffIndexed = canvasStaffImport.set_index(['login_id'])
canvasStaffandStudentsIndexed = google_connect.pd.concat([canvasStudentIndexed, canvasStaffIndexed], axis=0)