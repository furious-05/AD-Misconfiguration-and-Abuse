| Abuse Type                        | Description                                                                                                      |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **GenericAll**                    | Full control over the object. Allows resetting passwords, adding users to groups, linking GPOs, etc.             |
| **GenericWrite**                  | Write access to multiple attributes (like `servicePrincipalName`, `scriptPath`, etc.).                           |
| **WriteOwner**                    | Allows changing the owner of the object, which can escalate to full control.                                     |
| **WriteDACL**                     | Allows modifying the DACL itself—can grant yourself any permission.                                              |
| **OwnsObject**                    | The owner can often grant themselves full control, depending on environment policies.                            |
| **AddMember / RemoveMember**      | Ability to add or remove users from a group (commonly abused with high-priv groups like Domain Admins).          |
| **Self-Membership**               | If a user can add themselves to a group, they can escalate privileges.                                           |
| **ForceChangePassword**           | Allows changing another user’s password without knowing the old one (used with `Set-ADAccountPassword`).         |
| **Replicating Directory Changes** | Grants ability to perform **DCSync** attacks (pull password hashes from DC).                                     |
| **WriteProperty**                 | Modify specific object properties, like `servicePrincipalName` (for SPN abuse).                                  |
| **ReadLAPSPassword**              | If a user has read access to the `ms-Mcs-AdmPwd` attribute, they can extract LAPS-managed local admin passwords. |
| **LinkGroupPolicy**               | Ability to link GPOs to OUs—can deploy malicious policies or startup scripts.                                    |
| **ModifyPermissions**             | Similar to WriteDACL; allows granting or denying permissions.                                                    |
