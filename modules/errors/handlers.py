def register_error_handlers(application):

    @application.errorhandler(500)
    def handle_500_error(error):
        return "An unexpected error has occurred: {}".format(error.message)
