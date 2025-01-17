import functools

# This code was taken from `sd-webui-neutral-prompt`` repo
# ref: https://github.com/ljleb/sd-webui-neutral-prompt

class ModuleHijacker:
    def __init__(self, module):
        self.__module = module
        self.__original_functions = {}

    def hijack(self, attribute):
        if attribute not in self.__original_functions:
            self.__original_functions[attribute] = getattr(self.__module, attribute)

        def decorator(function):
            setattr(self.__module, attribute, functools.partial(function, original_function=self.__original_functions[attribute]))
            return function

        return decorator

    def reset_module(self):
        for attribute, original_function in self.__original_functions.items():
            setattr(self.__module, attribute, original_function)

        self.__original_functions.clear()

    @staticmethod
    def install_or_get(module, hijacker_attribute, on_uninstall=lambda _callback: None):
        if hasattr(module, hijacker_attribute):
            return getattr(module, hijacker_attribute)
        module_hijacker = ModuleHijacker(module)
        setattr(module, hijacker_attribute, module_hijacker)
        on_uninstall(lambda: delattr(module, hijacker_attribute))
        on_uninstall(module_hijacker.reset_module)
        return module_hijacker
