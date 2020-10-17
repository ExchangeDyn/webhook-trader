import whtrader

application = whtrader.create_app()

if __name__ == "__main__":
    application.debug = True
    application.run()
