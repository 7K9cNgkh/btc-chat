import os

from cffi import FFI

BASE_DEFINITIONS = """
typedef struct secp256k1_context_struct secp256k1_context;

typedef struct {
    unsigned char data[64];
} secp256k1_pubkey;

typedef struct {
    unsigned char *msg_chat;
    unsigned char *pk_B;
    unsigned char *sk_A;
    unsigned char *vk_A;
} secp256k1_chat_data;

typedef struct {
    unsigned char data[64];
} secp256k1_ecdsa_signature;

typedef int (*secp256k1_nonce_function)(
    unsigned char *nonce32,
    const unsigned char *msg32,
    const unsigned char *key32,
    const unsigned char *algo16,
    void *data,
    unsigned int attempt
);

#define SECP256K1_FLAGS_TYPE_MASK 255
#define SECP256K1_FLAGS_TYPE_CONTEXT 1
#define SECP256K1_FLAGS_TYPE_COMPRESSION 2

#define SECP256K1_FLAGS_BIT_CONTEXT_VERIFY 256
#define SECP256K1_FLAGS_BIT_CONTEXT_SIGN 512
#define SECP256K1_FLAGS_BIT_COMPRESSION 256

#define SECP256K1_CONTEXT_VERIFY 257
#define SECP256K1_CONTEXT_SIGN 513
#define SECP256K1_CONTEXT_NONE 1

#define SECP256K1_EC_COMPRESSED 258
#define SECP256K1_EC_UNCOMPRESSED 2

secp256k1_context* secp256k1_context_create(
    unsigned int flags
);

secp256k1_context* secp256k1_context_clone(
    const secp256k1_context* ctx
);

void secp256k1_context_destroy(
    secp256k1_context* ctx
);

void secp256k1_context_set_illegal_callback(
    secp256k1_context* ctx,
    void (*fun)(const char* message, void* data),
    const void* data
);

void secp256k1_context_set_error_callback(
    secp256k1_context* ctx,
    void (*fun)(const char* message, void* data),
    const void* data
);

int secp256k1_ec_pubkey_parse(
    const secp256k1_context* ctx,
    secp256k1_pubkey* pubkey,
    const unsigned char *input,
    size_t inputlen
);

int secp256k1_ec_pubkey_serialize(
    const secp256k1_context* ctx,
    unsigned char *output,
    size_t *outputlen,
    const secp256k1_pubkey* pubkey,
    unsigned int flags
);

int secp256k1_ecdsa_signature_parse_compact(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature* sig,
    const unsigned char *input64
);

int secp256k1_ecdsa_signature_parse_der(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature* sig,
    const unsigned char *input,
    size_t inputlen
);

int secp256k1_ecdsa_signature_serialize_der(
    const secp256k1_context* ctx,
    unsigned char *output,
    size_t *outputlen,
    const secp256k1_ecdsa_signature* sig
);

int secp256k1_ecdsa_signature_serialize_compact(
    const secp256k1_context* ctx,
    unsigned char *output64,
    const secp256k1_ecdsa_signature* sig
);

int secp256k1_ecdsa_verify(
    const secp256k1_context* ctx,
    const secp256k1_ecdsa_signature *sig,
    const unsigned char *msg32,
    const secp256k1_pubkey *pubkey
);

int secp256k1_ecdsa_signature_normalize(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature *sigout,
    const secp256k1_ecdsa_signature *sigin
);

extern const secp256k1_nonce_function secp256k1_nonce_function_chat;

extern const secp256k1_nonce_function secp256k1_nonce_function_rfc6979;

extern const secp256k1_nonce_function secp256k1_nonce_function_default;

int secp256k1_ecdsa_sign(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature *sig,
    const unsigned char *msg32,
    const unsigned char *seckey,
    secp256k1_nonce_function noncefp,
    const void *ndata
);

int secp256k1_ec_seckey_verify(
    const secp256k1_context* ctx,
    const unsigned char *seckey
);

int secp256k1_ec_pubkey_create(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const unsigned char *seckey
);

int secp256k1_ec_privkey_tweak_add(
    const secp256k1_context* ctx,
    unsigned char *seckey,
    const unsigned char *tweak
);

int secp256k1_ec_pubkey_tweak_add(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const unsigned char *tweak
);

int secp256k1_ec_privkey_tweak_mul(
    const secp256k1_context* ctx,
    unsigned char *seckey,
    const unsigned char *tweak
);

int secp256k1_ec_pubkey_tweak_mul(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const unsigned char *tweak
);

int secp256k1_context_randomize(
    secp256k1_context* ctx,
    const unsigned char *seed32
);

int secp256k1_ec_pubkey_combine(
    const secp256k1_context* ctx,
    secp256k1_pubkey *out,
    const secp256k1_pubkey * const * ins,
    size_t n
);
"""

RECOVERY_DEFINITIONS = """
typedef struct {
    unsigned char data[65];
} secp256k1_ecdsa_recoverable_signature;

int secp256k1_ecdsa_recoverable_signature_parse_compact(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_recoverable_signature* sig,
    const unsigned char *input64,
    int recid
);

int secp256k1_ecdsa_recoverable_signature_convert(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature* sig,
    const secp256k1_ecdsa_recoverable_signature* sigin
);

int secp256k1_ecdsa_recoverable_signature_serialize_compact(
    const secp256k1_context* ctx,
    unsigned char *output64,
    int *recid,
    const secp256k1_ecdsa_recoverable_signature* sig
);

int secp256k1_ecdsa_sign_recoverable(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_recoverable_signature *sig,
    const unsigned char *msg32,
    const unsigned char *seckey,
    secp256k1_nonce_function noncefp,
    const void *ndata
);

int secp256k1_ecdsa_recover(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const secp256k1_ecdsa_recoverable_signature *sig,
    const unsigned char *msg32
);
"""

ECDH_DEFINITIONS = """
int secp256k1_ecdh(
  const secp256k1_context* ctx,
  unsigned char *result,
  const secp256k1_pubkey *pubkey,
  const unsigned char *privkey,
  void *hashfp,
  void *data
);
"""

AESNI_DEFINITIONS = """
void secp256k1_aesni_256_key_expansion (
  unsigned char *key,
  const unsigned char *userkey
);

void secp256k1_aesni_256_dec_key_expansion (
  unsigned char *dec_key,
  const unsigned char *key_sched
);

void secp256k1_aesni_ecb_encrypt (
  unsigned char *out,
  const unsigned char *in,
  unsigned long length,
  const unsigned char *key,
  int number_of_rounds
);

void secp256k1_aesni_cbc_encrypt (
  unsigned char *out,
  const unsigned char *in,
  const unsigned char ivec[16],
  unsigned long length,
  const unsigned char *key,
  int number_of_rounds
);

void secp256k1_aesni_ecb_decrypt (
  unsigned char *out,
  const unsigned char *in,
  unsigned long length,
  const unsigned char *key,
  int number_of_rounds
);

void secp256k1_aesni_cbc_decrypt(
  unsigned char *out,
  const unsigned char *in,
  const unsigned char ivec[16],
  unsigned long length,
  const unsigned char *key,
  int number_of_rounds
);
"""

ffi = FFI()

ffi.cdef(BASE_DEFINITIONS)
ffi.cdef(RECOVERY_DEFINITIONS)
ffi.cdef(ECDH_DEFINITIONS)
ffi.cdef(AESNI_DEFINITIONS)

here = os.path.dirname(os.path.abspath(__file__))
lib = ffi.dlopen(os.path.join(here, 'libsecp256k1.dll'))
