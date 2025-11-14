def allowed_file(filename, app_config):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app_config['ALLOWED_EXTENSIONS']