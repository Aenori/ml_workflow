
class AppConfig:
    df_limit_to_compress = 30000

    def __setattr__(self, k, v):
        if not hasattr(AppConfig, k):
            msg = f"ERROR : trying to set {k} for app_config, which is not allowed"
            msg += f"\nAllowed attr : {attr for attr in dir(AppConfig) if not attr.startswith('_')}"
            raise Exception(msg)
            
        if not isinstance(v, type(getattr(AppConfig, k))):
            msg = f"ERROR : invalid type for attr {k}\n"
            msg += f"It should be instance of {type(getattr(AppConfig, k))}"
            raise Exception(msg)

        self.__dict__[k] = v

app_config = AppConfig()
