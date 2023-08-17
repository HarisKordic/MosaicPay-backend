"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import {
	Button,
	Grid,
	Typography,
	FormHelperText,
	InputAdornment,
	IconButton,
} from "@mui/material";
import Image from "next/image";
import * as Yup from "yup";
import { VisibilityOff, Visibility } from "@mui/icons-material";
import { login } from "../api";
import Alert from "@mui/material/Alert";
import { dtoLogin } from "../dtos/dtoLogin";
import Link from "next/link";
import RootLayout from "../layout";

export default function Login() {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [validationErrors, setValidationErrors] = useState(Object);
	const [showPassword, setShowPassword] = useState(false);
	const [showAlert, setShowAlert] = useState(false);
	const router = useRouter();
	const { document } = window;
	const [serverErrorMessage, setServerErrorMessage] = useState("");
	const handleEmailChange = (event: any) => {
		setEmail(event.target.value);
	};

	const handlePasswordChange = (event: any) => {
		setPassword(event.target.value);
	};

	const handleShowPassword = () => {
		setShowPassword((prevShowPassword) => !prevShowPassword);
	};

	const validateForm = async () => {
		const schema = Yup.object().shape({
			email: Yup.string().email("Invalid email").required("Email is required"),
			password: Yup.string().required("Password is required"),
		});

		try {
			await schema.validate({ email, password }, { abortEarly: false });
			setValidationErrors({});
			return true;
		} catch (error: any) {
			const errors = {};
			error.inner.forEach((err: any) => {
				//@ts-ignore
				errors[err.path] = err.message;
			});
			setValidationErrors(errors);
			return false;
		}
	};
	const handleSubmit = async (event: any) => {
		event.preventDefault();
		if (await validateForm()) {
			const registration: dtoLogin = {
				email: email,
				password: password,
			};

			try {
				const result = await login(registration);
				document.cookie = `token=${result.token}; path=/`;
				router.push("/home");
			} catch (error: any) {
				setServerErrorMessage(error.response.data);
				setShowAlert(true);
			}
		}
	};

	return (
		<RootLayout>
			<Grid
				sx={{
					"& .MuiTextField-root": {
						m: 1.5,
						width: "auto",
						height: "100%",
						p: 0.5,
					},
				}}
				display={"flex"}
				justifyContent={"center"}
				flexDirection={"column"}
				flexWrap={"wrap"}
			>
				<Box
					sx={{
						display: "flex",
						justifyContent: "center",
						borderRadius: "80%",
						overflow: "hidden",
						width: "400px",
						height: "200px",
						margin: "0 auto",
						mt: 2,
					}}
				>
					<Image
						src="/images/MosaicPay_logo.png"
						alt="Logo"
						width={200}
						height={200}
					/>
				</Box>
				<Box display={"flex"} justifyContent={"center"} sx={{ mt: 2 }}>
					<Typography variant="h5" component="h5">
						Login
					</Typography>
				</Box>

				<TextField
					id="email"
					name="email"
					label="Email"
					placeholder="email@example.com"
					variant="outlined"
					value={email}
					onChange={handleEmailChange}
					color="secondary"
					error={!!validationErrors.email}
				/>
				{validationErrors.email && (
					<FormHelperText>{validationErrors.email}</FormHelperText>
				)}
				<TextField
					id="password"
					name="password"
					label="Password"
					variant="outlined"
					value={password}
					onChange={handlePasswordChange}
					color="secondary"
					type={showPassword ? "text" : "password"}
					error={!!validationErrors.password}
					InputProps={{
						endAdornment: (
							<InputAdornment position="end">
								<IconButton onClick={handleShowPassword}>
									{showPassword ? <VisibilityOff /> : <Visibility />}
								</IconButton>
							</InputAdornment>
						),
					}}
				/>
				{validationErrors.password && (
					<FormHelperText>{validationErrors.password}</FormHelperText>
				)}
				<Box
					sx={{ mt: 1, ml: 1, width: "100%" }}
					display={"flex"}
					justifyContent={"flex-start"}
					flexWrap={"wrap"}
					flexDirection={"column"}
				>
					<Typography component="p">Don't have an account? </Typography>
					<Link href={"/signup"} onClick={() => router.push("/signup")}>
						Sign up
					</Link>
				</Box>
				<Button
					sx={{ width: "50%", mr: "auto", ml: "auto", mt: 5 }}
					variant="contained"
					type="submit"
					color="secondary"
					onClick={handleSubmit}
				>
					Login
				</Button>
				<Alert
					sx={{ mt: 5, display: showAlert ? "flex" : "none" }}
					action={
						<Button
							color="error"
							size="small"
							onClick={() => setShowAlert(false)}
						>
							X
						</Button>
					}
					onClose={() => setShowAlert(false)}
					severity="error"
				>
					{serverErrorMessage}
				</Alert>
			</Grid>
		</RootLayout>
	);
}
