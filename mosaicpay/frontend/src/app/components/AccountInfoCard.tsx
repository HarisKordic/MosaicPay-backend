import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { useRouter } from "next/router";

const bull = (
	<Box
		component="span"
		sx={{ display: "inline-block", mx: "2px", transform: "scale(0.8)" }}
	>
		•
	</Box>
);

interface IAccountInfoCardProps {
	balance: string;
	date: string;
	accountId?: string;
	showDetail?: boolean;
}
export default function AccountInfoCard(props: IAccountInfoCardProps) {
	const router = useRouter();
	return (
		<Card elevation={14} sx={{ width: "100%" }}>
			<CardContent>
				<Typography
					fontWeight={"bold"}
					sx={{ fontSize: 16, mb: 2, textAlign: "center" }}
					color="text.secondary"
				>
					Balance
				</Typography>
				<Typography sx={{ mb: 4 }} variant="h5" component="div">
					{props.balance || "no current information"} {" $"}
				</Typography>
				<Typography sx={{ mb: 1.5 }} color="text.secondary">
					{props.date || "no date information"}
				</Typography>
				<Box display={"flex"} justifyContent={"center"} mt={3}>
					<Button
						sx={{ display: `${props.showDetail ? "block" : "none"}` }}
						onClick={() => router.push(`/edit-account/${props.accountId}`)}
						size="small"
						color="secondary"
						variant="outlined"
					>
						View account
					</Button>
				</Box>
			</CardContent>
		</Card>
	);
}
