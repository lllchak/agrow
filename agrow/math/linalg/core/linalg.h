#ifndef __LINALG_CORE_LINALG_H__
#define __LINALG_CORE_LINALG_H__

namespace agrow {
    template <typename T, size_t Size>
    class ag_vector {
    private:
        T m_data[Size];

    public:
        ag_vector()
        {
        }
    };
}  // agrow

#endif  // __LINALG_CORE_LINALG_H__