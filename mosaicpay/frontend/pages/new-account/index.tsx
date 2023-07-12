import {
	Alert,
	Box,
	Button,
	Container,
	Grid,
	TextField,
	Typography,
} from "@mui/material";
import { Cancel, Save } from "@mui/icons-material";
import { useRouter } from "next/navigation";
import { useState } from "react";
import * as yup from "yup";
import { getUser, postNewAccount } from "../../src/app/api";
import AccountMenu from "@/app/components/AccountMenu";
import Media from "@/app/components/Media";

export default function NewAccount() {
	const router = useRouter();
	const [accountName, setAccountName] = useState("");
	const [balance, setBalance] = useState("");
	const [validationErrors, setValidationErrors] = useState(Object);
	const [showAlert, setShowAlert] = useState(false);
	const [userId, setUserId] = useState(0);
	const [accountId, setAccountId] = useState();
	const [type, setType] = useState("");
	const [url, setUrl] = useState();
	const [documentId, setDocumentId] = useState(0);
	const [disableFileUpload, setDisableFileUpload] = useState(true);

	const validationSchema = yup.object().shape({
		accountName: yup
			.string()
			.required("Account name is required")
			.max(255, "Maximum length of the account name is 255 characters")
			.min(5, "Minimum length of the account name is 5"),
		balance: yup
			.number()
			.typeError("Balance must be a number")
			.required("Balance is required"),
	});

	const handleAccountNameChange = (event: any) => {
		setAccountName(event.target.value);
	};

	const handleBalanceChange = (event: any) => {
		setBalance(event.target.value);
	};

	const validateForm = async (): Promise<boolean> => {
		try {
			await validationSchema.validate(
				{ accountName, balance },
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

	const handleSubmit = async (event: any) => {
		event.preventDefault();
		if (await validateForm()) {
			try {
				const user = await getUser();
				let account: dtoAccount = {
					name: accountName,
					balance: Number.parseFloat(balance),
					user: user?.user_id,
				};
				const result = await postNewAccount(account);

				setShowAlert(true);
				setDisableFileUpload(false);
				setUserId(result.user);
				setDocumentId(0);
				setAccountId(result.account_id);
			} catch (error) {}
		}
	};
	return (
		<Container disableGutters>
			<Box display={"flex"} justifyContent={"center"} mb={3}>
				<AccountMenu></AccountMenu>
			</Box>
			<Grid
				display="flex"
				flexDirection="column"
				width="100%"
				height="100%"
				justifyContent="center"
			>
				<Box>
					<Typography
						variant="h4"
						component="h4"
						mb={3}
						sx={{ textAlign: "center" }}
					>
						Add account
					</Typography>
				</Box>
				<Box width="100%" padding={2}>
					<TextField
						sx={{ mb: 2 }}
						fullWidth
						id="account-name"
						name="accountName"
						label="Account name"
						placeholder="Savings account"
						variant="outlined"
						color="secondary"
						value={accountName}
						onChange={handleAccountNameChange}
						error={!!validationErrors.accountName}
						helperText={validationErrors.accountName}
					/>

					<TextField
						sx={{ mb: 2 }}
						fullWidth
						id="balance"
						name="balance"
						placeholder="784578.45"
						label="Balance"
						variant="outlined"
						color="secondary"
						value={balance}
						onChange={handleBalanceChange}
						error={!!validationErrors.balance}
						helperText={validationErrors.balance}
					/>

					<Box
						display={`${disableFileUpload ? "none" : "block"}`}
						justifyContent={"center"}
						sx={{ mt: 5 }}
					>
						<Media
							accountId={accountId}
							userId={userId?.toString()}
							url={url}
							type={type}
							documentId={documentId}
						></Media>
					</Box>
					<Box
						display={"flex"}
						justifyContent={"space-between"}
						sx={{ mt: 10 }}
					>
						<Button
							startIcon={<Save></Save>}
							color="secondary"
							variant="outlined"
							onClick={handleSubmit}
						>
							Save
						</Button>
						<Button
							startIcon={<Cancel></Cancel>}
							color="secondary"
							variant="outlined"
							onClick={() => router.push("/home")}
						>
							Cancel
						</Button>
					</Box>
					<Alert
						sx={{ mt: 5, display: showAlert ? "flex" : "none" }}
						action={
							<Button
								color="success"
								size="small"
								onClick={() => setShowAlert(false)}
							>
								X
							</Button>
						}
						onClose={() => setShowAlert(false)}
						severity="success"
					>
						Account successfuly created!
					</Alert>
				</Box>
			</Grid>
		</Container>
	);
}
