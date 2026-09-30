#pragma once

// Custom builds may change the no-aiding observation-noise ceiling.
// Stock firmware retains the existing 50 m limit.
#ifndef EK3_NOAID_M_NSE_MAX
#define EK3_NOAID_M_NSE_MAX 50.0f
#endif

static_assert(EK3_NOAID_M_NSE_MAX >= 0.5f && EK3_NOAID_M_NSE_MAX <= 10000.0f,
              "EK3_NOAID_M_NSE_MAX must be between 0.5 and 10000 m");
