// SPDX-License-Identifier: MPL-2.0
// SPDX-FileCopyrightText: 2023 igo95862

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <linux/nsfs.h>
#include <sched.h>
#include <sys/ioctl.h>

#define CALL_PYTHON_FAIL_ACTION(py_function, action) \
        ({                                           \
                PyObject* new_object = py_function;  \
                if (new_object == NULL) {            \
                        action;                      \
                }                                    \
                new_object;                          \
        })

#define CALL_PYTHON_AND_CHECK(py_function) CALL_PYTHON_FAIL_ACTION(py_function, return NULL)

#define CALL_PYTHON_INT_CHECK(py_function)    \
        ({                                    \
                int return_int = py_function; \
                if (return_int < 0) {         \
                        return NULL;          \
                }                             \
                return_int;                   \
        })

#define CALL_PYTHON_BOOL_CHECK(py_function)   \
        ({                                    \
                int return_int = py_function; \
                if (!return_int) {            \
                        return NULL;          \
                }                             \
                return_int;                   \
        })

__attribute__((used)) static inline void PyObject_cleanup(PyObject** object) {
        Py_XDECREF(*object);
}

#define CLEANUP_PY_OBJECT __attribute__((cleanup(PyObject_cleanup)))

static PyObject* LxnsOs_unshare(PyObject* Py_UNUSED(self), PyObject* args) {
        int flags = 0;

        CALL_PYTHON_BOOL_CHECK(PyArg_ParseTuple(args, "i", &flags, NULL));
        if (unshare(flags) == -1) {
                return PyErr_SetFromErrno(PyExc_OSError);
        }
        Py_RETURN_NONE;
}

static PyObject* LxnsOs_setns(PyObject* Py_UNUSED(self), PyObject* args) {
        int fd = -1, nstype = -1;

        CALL_PYTHON_BOOL_CHECK(PyArg_ParseTuple(args, "ii", &fd, &nstype, NULL));
        if (setns(fd, nstype) == -1) {
                return PyErr_SetFromErrno(PyExc_OSError);
        }
        Py_RETURN_NONE;
}

static PyObject* LxnsOs_ns_get_userns(PyObject* Py_UNUSED(self), PyObject* args) {
        int fd = -1;

        CALL_PYTHON_BOOL_CHECK(PyArg_ParseTuple(args, "i", &fd, NULL));

        int userns = ioctl(fd, NS_GET_USERNS);
        if (userns == -1) {
                return PyErr_SetFromErrno(PyExc_OSError);
        }

        return Py_BuildValue("i", userns, NULL);
};

static PyObject* LxnsOs_ns_get_parent(PyObject* Py_UNUSED(self), PyObject* args) {
        int fd = -1;

        CALL_PYTHON_BOOL_CHECK(PyArg_ParseTuple(args, "i", &fd, NULL));

        int ns_type = ioctl(fd, NS_GET_PARENT);
        if (ns_type == -1) {
                return PyErr_SetFromErrno(PyExc_OSError);
        }

        return Py_BuildValue("i", ns_type, NULL);
};

static PyObject* LxnsOs_ns_get_nstype(PyObject* Py_UNUSED(self), PyObject* args) {
        int fd = -1;

        CALL_PYTHON_BOOL_CHECK(PyArg_ParseTuple(args, "i", &fd, NULL));

        int ns_type = ioctl(fd, NS_GET_NSTYPE);
        if (ns_type == -1) {
                return PyErr_SetFromErrno(PyExc_OSError);
        }

        return Py_BuildValue("i", ns_type, NULL);
};

static PyObject* LxnsOs_ns_get_owner_uid(PyObject* Py_UNUSED(self), PyObject* args) {
        int fd = -1;

        CALL_PYTHON_BOOL_CHECK(PyArg_ParseTuple(args, "i", &fd, NULL));

        uid_t uid = -1;
        int r = ioctl(fd, NS_GET_OWNER_UID, &uid);
        if (r == -1) {
                return PyErr_SetFromErrno(PyExc_OSError);
        }

        return Py_BuildValue("I", uid, NULL);
};

static PyMethodDef lxns_os_methods[] = {
    {"unshare", (PyCFunction)LxnsOs_unshare, METH_VARARGS, NULL},
    {"setns", (PyCFunction)LxnsOs_setns, METH_VARARGS, NULL},
    {"ns_get_userns", (PyCFunction)LxnsOs_ns_get_userns, METH_VARARGS, NULL},
    {"ns_get_parent", (PyCFunction)LxnsOs_ns_get_parent, METH_VARARGS, NULL},
    {"ns_get_nstype", (PyCFunction)LxnsOs_ns_get_nstype, METH_VARARGS, NULL},
    {"ns_get_owner_uid", (PyCFunction)LxnsOs_ns_get_owner_uid, METH_VARARGS, NULL},
    {0},
};

static PyModuleDef lxns_os_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "os",
    .m_size = -1,
    .m_methods = lxns_os_methods,
};

PyMODINIT_FUNC PyInit_os(void) {
        PyObject* m CLEANUP_PY_OBJECT = CALL_PYTHON_AND_CHECK(PyModule_Create(&lxns_os_module));

        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_FILES", CLONE_FILES));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_FS", CLONE_FS));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWCGROUP", CLONE_NEWCGROUP));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWIPC", CLONE_NEWIPC));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWNET", CLONE_NEWNET));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWNS", CLONE_NEWNS));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWPID", CLONE_NEWPID));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWTIME", CLONE_NEWTIME));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWUSER", CLONE_NEWUSER));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_NEWUTS", CLONE_NEWUTS));
        CALL_PYTHON_INT_CHECK(PyModule_AddIntConstant(m, "CLONE_SYSVSEM", CLONE_SYSVSEM));

        Py_INCREF(m);
        return m;
}
