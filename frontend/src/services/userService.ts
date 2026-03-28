import api from "@/lib/axios";

export const userService = {
    uploadAvatar: async (formdata: FormData) => {
        const res = await api.post("/users/avatar", formdata, {
            headers: {"Content-Type": "multipart/form-data"},
        });

        if (res.status === 400) {
            throw new Error("Error while updating avatar");
        }   

        return res.data;
    }
}