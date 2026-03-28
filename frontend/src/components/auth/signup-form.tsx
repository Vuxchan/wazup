import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Label } from "../ui/label"
import { useAuthStore } from "@/stores/useAuthStore"
import { useNavigate } from "react-router"

const signUpSchema = z.object({
    firstname: z.string().min(1, "First name is required"),
    lastname: z.string().min(1, "Last name is required"),
    username: z.string().min(3, "Username must have at least 3 letters"),
    email: z.email("Invalid email"),
    password: z.string().min(6, "Password must have at least 6 letters")
});

type SignUpFormValues = z.infer<typeof signUpSchema>

export function SignupForm({
    className,
    ...props
}: React.ComponentProps<"div">) {
    const { signUp } = useAuthStore();
    const navigate = useNavigate();
    const {register, handleSubmit, formState: {errors, isSubmitting}} = useForm<SignUpFormValues>({
        resolver: zodResolver(signUpSchema)
    });

    const onSubmit = async (data: SignUpFormValues) => {
        const {firstname, lastname, username, email, password} = data;

        await signUp(username, password, email, firstname, lastname);

        navigate("/signin");
    }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
        <Card className="overflow-hidden p-0 border-border">
            <CardContent className="grid p-0 md:grid-cols-2">
            <form className="p-6 md:p-8" onSubmit={handleSubmit(onSubmit)}>
                <div className="flex flex-col gap-6">
                <div className="flex flex-col items-center text-center gap-2">
                    <a href="/" className="mx-auto block w-fit text-center">
                    <img className="size-30" src="/logo.png" alt="logo"/>
                    </a>

                    <h1 className="text-2xl font-bold">Create Wazup account</h1>
                    <p className="text-mutex-foreground text-balance">Welcome! Let's sign in to start</p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-2">
                    <Label htmlFor="lastname" className="block text-sm">
                        Last name
                    </Label>
                    <Input type="text" id="lastname" {...register("lastname")}/>
                    {errors.lastname && (
                        <p className="error-message">
                        {errors.lastname.message}
                        </p>
                    )}
                    </div>

                    <div className="space-y-2">
                    <Label htmlFor="firstname" className="block text-sm">
                        First name
                    </Label>
                    <Input type="text" id="firstname" {...register("firstname")}/>
                    {errors.firstname && (
                        <p className="error-message">
                        {errors.firstname.message}
                        </p>
                    )}
                    </div>
                </div>

                <div className="flex flex-col gap-3">
                    <Label htmlFor="username" className="block text-sm">
                    Username
                    </Label>
                    <Input type="text" id="username" placeholder="Wazup" {...register("username")}/>
                    {errors.username && (
                    <p className="error-message">
                        {errors.username.message}
                    </p>
                    )}
                </div>

                <div className="flex flex-col gap-3">
                    <Label htmlFor="email" className="block text-sm">
                    Email
                    </Label>
                    <Input type="email" id="email" placeholder="m@gmail.com" {...register("email")}/>
                    {errors.email && (
                    <p className="error-message">
                        {errors.email.message}
                    </p>
                    )}
                </div>

                <div className="flex flex-col gap-3">
                    <Label htmlFor="password" className="block text-sm">
                    Password
                    </Label>
                    <Input type="password" id="password" {...register("password")}/>
                    {errors.password && (
                    <p className="error-message">
                        {errors.password.message}
                    </p>
                    )}
                </div>

                <Button type="submit" className="w-full" disabled={isSubmitting}>
                    Create your account
                </Button>

                <div className="text-center text-sm">
                    Already have an account! {""}
                    <a href="/signin" className="underline underline-offset-4">
                    Sign in
                    </a>
                </div>

                </div>
            </form>
            <div className="relative hidden bg-muted md:block">
                <img
                src="/placeholderSignUp.png"
                alt="Image"
                className="absolute top-1/2 -translate-y-1/2 object-cover"
                />
            </div>
            </CardContent>
        </Card>
        <div className="text-xs text-balance px-6 text-center *:[a]:hover:text-primary text-muted-foreground *:[a]:underline *:[a]:underline-offset-4">
            By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
            and <a href="#">Privacy Policy</a>.
        </div>
    </div>
    )
}
