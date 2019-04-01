# -*- coding: utf-8 -*-

import unohelper
from ext_gen import options_dialog

IMPLEMENTATION_NAME = "com.palaceweb.ext_gen.IM"
SERVICE_NAME = "com.palaceweb.ext_gen.service"


def create(ctx, *args):
    return options_dialog.create(
        ctx,
        implementation_name=IMPLEMENTATION_NAME,
        service_name=SERVICE_NAME,
        *args
    )


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    create, IMPLEMENTATION_NAME, (SERVICE_NAME,),
)
