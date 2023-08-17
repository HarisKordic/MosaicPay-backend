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
import { dtoRegister } from "../../src/app/dtos/dtoRegistser";
import { register } from "../../src/app/api";
import Alert from "@mui/material/Alert";
import Link from "next/link";

export default function Signup() {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [passwordRepeat, setPasswordRepeat] = useState("");
	const [validationErrors, setValidationErrors] = useState(Object);
	const [showPassword, setShowPassword] = useState(false);
	const [showPasswordRepeat, setShowPasswordRepeat] = useState(false);
	const [showAlert, setShowAlert] = useState(false);
	const router = useRouter();
	const handleEmailChange = (event: any) => {
		setEmail(event.target.value);
	};

	const handlePasswordChange = (event: any) => {
		setPassword(event.target.value);
	};

	const handlePasswordRepeatChange = (event: any) => {
		setPasswordRepeat(event.target.value);
	};

	const handleShowPassword = () => {
		setShowPassword((prevShowPassword) => !prevShowPassword);
	};

	const handleShowPasswordRepeat = () => {
		setShowPasswordRepeat((prevShowPasswordRepeat) => !prevShowPasswordRepeat);
	};

	const validateForm = async () => {
		const schema = Yup.object().shape({
			email: Yup.string().email("Invalid email").required("Email is required"),
			password: Yup.string()
				.min(8, "Password must be at least 8 characters")
				.required("Password is required"),
			passwordRepeat: Yup.string()
				.oneOf([Yup.ref("password")], "Passwords must match")
				.required("Repeat password is required"),
		});

		try {
			await schema.validate(
				{ email, password, passwordRepeat },
				{ abortEarly: false }
			);
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
	const serverErrorMessage =
		"User with the same email already exists! Please, try another email.";
	const handleSubmit = async (event: any) => {
		event.preventDefault();
		if (await validateForm()) {
			const registration: dtoRegister = {
				email: email,
				password: password,
			};

			try {
				const result = await register(registration);
				if (!result) {
				} else {
					router.push("/login");
				}
			} catch (error) {
				setShowAlert(true);
			}
		}
	};

	return (
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
					Sign up
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
				helperText="* Password should be at least 8 characters long. Use numbers, letters, special characters and capitals."
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

			<TextField
				id="password-repeat"
				name="passwordRepeat"
				label="Repeat password"
				variant="outlined"
				value={passwordRepeat}
				onChange={handlePasswordRepeatChange}
				color="secondary"
				type={showPasswordRepeat ? "text" : "password"}
				error={!!validationErrors.passwordRepeat}
				InputProps={{
					endAdornment: (
						<InputAdornment position="end">
							<IconButton onClick={handleShowPasswordRepeat}>
								{showPasswordRepeat ? <VisibilityOff /> : <Visibility />}
							</IconButton>
						</InputAdornment>
					),
				}}
			/>
			{validationErrors.passwordRepeat && (
				<FormHelperText>{validationErrors.passwordRepeat}</FormHelperText>
			)}
			<Box
				sx={{ mt: 1, ml: 1, width: "100%" }}
				display={"flex"}
				justifyContent={"flex-start"}
				flexWrap={"wrap"}
				flexDirection={"column"}
			>
				<Typography component="p">Already have an account? </Typography>
				<Link href={"/login"} onClick={() => router.push("/login")}>
					Login
				</Link>
			</Box>
			<Button
				sx={{ width: "50%", mr: "auto", ml: "auto", mt: 5 }}
				variant="contained"
				type="submit"
				color="secondary"
				onClick={handleSubmit}
			>
				Sign up
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
	);
}
