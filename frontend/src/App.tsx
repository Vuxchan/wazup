import {BrowserRouter, Route, Routes} from "react-router"
import SignInPage from "./pages/SigninPage";
import SignUpPage from "./pages/SignupPage";
import ChatAppPage from "./pages/ChatAppPage";
import {Toaster} from "sonner"
import ProtectedRoute from "./components/auth/ProtectedRoute";

function App() {
    return <>
        <Toaster/>
        <BrowserRouter>
            <Routes>
                {/* public routes */}
                <Route
                    path='/signin'
                    element={<SignInPage/>}
                />

                <Route
                    path='/signup'
                    element={<SignUpPage/>}
                />

                {/* protected routes */}
                <Route element={<ProtectedRoute/>}>
                    <Route
                        path='/'
                        element={<ChatAppPage/>}
                    />
                </Route>

            </Routes>
        </BrowserRouter>
    </>;
}

export default App
