import {
  Center,
  createStyles,
  Navbar,
  Stack,
  Tooltip,
  UnstyledButton,
} from "@mantine/core";
import {
  IconGauge,
  IconHome2,
  IconVectorBezierCircle,
  TablerIcon,
} from "@tabler/icons";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";

const useStyles = createStyles((theme) => ({
  link: {
    width: 50,
    height: 50,
    borderRadius: theme.radius.md,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color:
      theme.colorScheme === "dark"
        ? theme.colors.dark[0]
        : theme.colors.gray[7],

    "&:hover": {
      backgroundColor:
        theme.colorScheme === "dark"
          ? theme.colors.dark[5]
          : theme.colors.gray[0],
    },
  },

  active: {
    "&, &:hover": {
      backgroundColor: theme.fn.variant({
        variant: "light",
        color: theme.primaryColor,
      }).background,
      color: theme.fn.variant({ variant: "light", color: theme.primaryColor })
        .color,
    },
  },
}));

interface NavbarLinkProps {
  icon: TablerIcon;
  label: string;
  active?: boolean;
  onClick?(): void;
}

function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
  const { classes, cx } = useStyles();
  return (
    <Tooltip label={label} position="right" transitionDuration={0}>
      <UnstyledButton
        onClick={onClick}
        className={cx(classes.link, { [classes.active]: active })}
      >
        <Icon stroke={1.5} />
      </UnstyledButton>
    </Tooltip>
  );
}

export const NavbarMinimal = () => {
  const router = useRouter();
  const [active, setActive] = useState(2);
  const linksConfig = [
    { icon: IconHome2, label: "Home", href: "/" },
    { icon: IconGauge, label: "Dashboard", href: "/dashboard" },
    {
      icon: IconVectorBezierCircle,
      label: "Graph Viewer",
      href: "/graph-viewer",
    },
  ];

  return (
    <Navbar height={"100vh"} width={{ base: 80 }} p="md">
      <Center>
        <Image
          height={42}
          width={40}
          alt="Jaseci Logo"
          src="/Jaseci-Submark.png"
        ></Image>
      </Center>
      <Navbar.Section grow mt={50}>
        <Stack justify="center" spacing={0}>
          {linksConfig.map((link, index) => (
            <NavbarLink
              key={link.label}
              active={index === active}
              onClick={() => {
                setActive(index);
                router.push(link.href);
              }}
              icon={link.icon}
              label={link.label}
            />
          ))}
        </Stack>
      </Navbar.Section>
      <Navbar.Section>
        <Stack justify="center" spacing={0}>
          {/* <NavbarLink icon={IconSwitchHorizontal} label="Change server" /> */}
          {/* <NavbarLink icon={IconLogout} label="Logout" /> */}
        </Stack>
      </Navbar.Section>
    </Navbar>
  );
};
